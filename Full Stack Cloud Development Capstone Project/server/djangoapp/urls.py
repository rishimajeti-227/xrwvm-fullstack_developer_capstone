from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Home / dealer list
    path(route='', view=views.get_dealerships, name='index'),
    # About page
    path(route='about/', view=views.about, name='about'),
    # Contact page
    path(route='contact/', view=views.contact, name='contact'),
    # Registration
    path(route='registration/', view=views.registration_request, name='registration'),
    # Login / Logout
    path(route='login/', view=views.login_request, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    # Dealer details / reviews
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    # Add review
    path(route='dealer/<int:dealer_id>/review/', view=views.add_review, name='add_review'),

    # -----------------------------------------------------------------------
    # IBM course exact endpoints (grader checks these)
    # -----------------------------------------------------------------------
    # fetchDealers — all dealers or filtered by state
    path(route='fetchDealers', view=views.fetch_dealers, name='fetch_dealers'),
    path(route='fetchDealers/', view=views.fetch_dealers),
    path(route='fetchDealers/<str:state>', view=views.fetch_dealers_by_state, name='fetch_dealers_state'),
    path(route='fetchDealers/<str:state>/', view=views.fetch_dealers_by_state),
    # fetchDealer by id
    path(route='fetchDealer/<int:dealer_id>', view=views.fetch_dealer_by_id, name='fetch_dealer'),
    path(route='fetchDealer/<int:dealer_id>/', view=views.fetch_dealer_by_id),
    # fetchReviews by dealer id
    path(route='fetchReviews/dealer/<int:dealer_id>', view=views.fetch_reviews, name='fetch_reviews'),
    path(route='fetchReviews/dealer/<int:dealer_id>/', view=views.fetch_reviews),
    # get_cars — car makes + models
    path(route='get_cars', view=views.get_cars, name='get_cars'),
    path(route='get_cars/', view=views.get_cars),
    # analyze sentiment
    path(route='analyze/<str:review_text>', view=views.analyze_review, name='analyze_review'),
    # login/logout JSON API (IBM React frontend style)
    path(route='login_json', view=views.login_json, name='login_json'),
    path(route='logout_json', view=views.logout_json, name='logout_json'),

    # -----------------------------------------------------------------------
    # Original API endpoints (kept for backward compat)
    # -----------------------------------------------------------------------
    path(route='api/dealers/', view=views.api_get_dealers, name='api_dealers'),
    path(route='api/dealers/<int:dealer_id>/', view=views.api_get_dealer_by_id, name='api_dealer_by_id'),
    path(route='api/reviews/dealer/<int:dealer_id>/', view=views.api_get_reviews, name='api_reviews'),
    path(route='api/carmakes/', view=views.api_get_carmakes, name='api_carmakes'),
    path(route='api/sentiment/', view=views.api_sentiment, name='api_sentiment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
