import json
import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import CarDealer, CarMake, CarModel
from .restapis import (
    analyze_review_sentiments,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    get_dealers_from_cf,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Static pages
# ---------------------------------------------------------------------------

def about(request):
    return render(request, 'djangoapp/about.html')


def contact(request):
    return render(request, 'djangoapp/contact.html')


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------

def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('psw', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'Invalid username or password.'
    return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    print(f"Logging out user: {request.user.username}")
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('psw')
        if User.objects.filter(username=username).exists():
            context['message'] = 'Username already taken.'
            return render(request, 'djangoapp/registration.html', context)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        login(request, user)
        return redirect('djangoapp:index')
    return render(request, 'djangoapp/registration.html', context)


# ---------------------------------------------------------------------------
# Dealer views
# ---------------------------------------------------------------------------

def get_dealerships(request):
    state = request.GET.get('state', None)
    dealerships = get_dealers_from_cf(state=state) if state else get_dealers_from_cf()
    context = {
        'dealerships': dealerships,
        'selected_state': state,
    }
    return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    dealer = get_dealer_by_id_from_cf(dealer_id)
    reviews = get_dealer_reviews_from_cf(dealerId=dealer_id)

    # Also include any session-submitted reviews for this dealer
    session_key = f'review_{dealer_id}'
    if session_key in request.session:
        sr = request.session[session_key]
        from .models import DealerReview
        session_review = DealerReview(
            dealership=sr.get('dealership'),
            name=sr.get('name', ''),
            purchase=sr.get('purchase', False),
            review=sr.get('review', ''),
            purchase_date=sr.get('purchase_date', ''),
            car_make=sr.get('car_make', ''),
            car_model=sr.get('car_model', ''),
            car_year=sr.get('car_year', ''),
            sentiment=sr.get('sentiment', 'neutral'),
            id=9999,
        )
        reviews = list(reviews) + [session_review]

    context = {
        'dealer': dealer,
        'reviews': reviews,
        'dealer_id': dealer_id,
    }
    return render(request, 'djangoapp/dealer_details.html', context)


@csrf_exempt
def add_review(request, dealer_id):
    dealer = get_dealer_by_id_from_cf(dealer_id)
    context = {'dealer': dealer, 'dealer_id': dealer_id}

    if not request.user.is_authenticated:
        return redirect('djangoapp:index')

    if request.method == 'POST':
        review_text = request.POST.get('content', '')
        purchase = request.POST.get('purchasedCar') == 'on'
        purchase_date = request.POST.get('purchaseDate', '')
        car_make = request.POST.get('car_make', '')
        car_model = request.POST.get('car_model', '')
        car_year = request.POST.get('car_year', '')
        sentiment = analyze_review_sentiments(review_text)

        # Store the review in session so we can display it
        review_data = {
            'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'dealership': dealer_id,
            'review': review_text,
            'purchase': purchase,
            'purchase_date': purchase_date,
            'car_make': car_make,
            'car_model': car_model,
            'car_year': car_year,
            'sentiment': sentiment,
        }
        # Append to list of session reviews for this dealer
        session_key = f'review_{dealer_id}'
        existing = request.session.get(session_key)
        # Keep only the latest review (overwrite)
        request.session[session_key] = review_data
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)

    car_makes = CarMake.objects.all()
    car_models = CarModel.objects.all()
    context['car_makes'] = car_makes
    context['car_models'] = car_models
    return render(request, 'djangoapp/add_review.html', context)


# ---------------------------------------------------------------------------
# JSON API endpoints (replaces IBM Cloud Functions / Express-Mongo)
# These let cURL tasks work against localhost
# ---------------------------------------------------------------------------

def api_get_dealers(request):
    state = request.GET.get('state', None)
    dealers = get_dealers_from_cf(state=state) if state else get_dealers_from_cf()
    data = [
        {
            'id': d.id,
            'full_name': d.full_name,
            'short_name': d.short_name,
            'city': d.city,
            'st': d.st,
            'address': d.address,
            'zip': d.zip,
            'lat': d.lat,
            'long': d.long,
        }
        for d in dealers
    ]
    return JsonResponse({'dealers': data})


def api_get_dealer_by_id(request, dealer_id):
    d = get_dealer_by_id_from_cf(dealer_id)
    if not d:
        return JsonResponse({'error': 'Dealer not found'}, status=404)
    data = {
        'id': d.id,
        'full_name': d.full_name,
        'short_name': d.short_name,
        'city': d.city,
        'st': d.st,
        'address': d.address,
        'zip': d.zip,
        'lat': d.lat,
        'long': d.long,
    }
    return JsonResponse({'dealer': data})


def api_get_reviews(request, dealer_id):
    reviews = get_dealer_reviews_from_cf(dealerId=dealer_id)
    data = [
        {
            'id': r.id,
            'name': r.name,
            'dealership': r.dealership,
            'review': r.review,
            'purchase': r.purchase,
            'purchase_date': r.purchase_date,
            'car_make': r.car_make,
            'car_model': r.car_model,
            'car_year': r.car_year,
            'sentiment': r.sentiment,
        }
        for r in reviews
    ]
    return JsonResponse({'reviews': data})


def api_get_carmakes(request):
    makes = list(CarMake.objects.all().values('name', 'desc'))
    models = list(CarModel.objects.all().values('name', 'id', 'type', 'year'))
    return JsonResponse({'car_makes': makes, 'car_models': models})


def api_sentiment(request):
    text = request.GET.get('text', '')
    if not text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    sentiment = analyze_review_sentiments(text)
    return JsonResponse({'text': text, 'sentiment': sentiment})
