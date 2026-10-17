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
    # Login
    path(route='login/', view=views.login_request, name='login'),
    # Logout
    path(route='logout/', view=views.logout_request, name='logout'),
    # Dealer details / reviews
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    # Add review
    path(route='dealer/<int:dealer_id>/review/', view=views.add_review, name='add_review'),

    # --- JSON API endpoints (replaces Express/Mongo) ---
    path(route='api/dealers/', view=views.api_get_dealers, name='api_dealers'),
    path(route='api/dealers/<int:dealer_id>/', view=views.api_get_dealer_by_id, name='api_dealer_by_id'),
    path(route='api/reviews/dealer/<int:dealer_id>/', view=views.api_get_reviews, name='api_reviews'),
    path(route='api/carmakes/', view=views.api_get_carmakes, name='api_carmakes'),
    path(route='api/sentiment/', view=views.api_sentiment, name='api_sentiment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
