import json
import os
import requests
from .models import CarDealer, DealerReview

# Path to local JSON data files (used instead of IBM Cloud Functions)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLOUDANT_DATA = os.path.join(os.path.dirname(BASE_DIR), 'cloudant', 'data')


def _load_dealerships():
    """Load dealership data from local JSON file."""
    fpath = os.path.join(CLOUDANT_DATA, 'dealerships.json')
    with open(fpath, 'r') as f:
        data = json.load(f)
    return data.get('dealerships', [])


def _load_reviews():
    """Load review data from local JSON file."""
    fpath = os.path.join(CLOUDANT_DATA, 'reviews.json')
    with open(fpath, 'r') as f:
        data = json.load(f)
    return data.get('reviews', [])


def get_dealers_from_cf(url=None, **kwargs):
    """Return all dealers as CarDealer objects. Uses local JSON data."""
    results = []
    dealers = _load_dealerships()
    state = kwargs.get('state')
    for d in dealers:
        if state and d.get('st') != state:
            continue
        dealer_obj = CarDealer(
            address=d['address'],
            city=d['city'],
            full_name=d['full_name'],
            id=d['id'],
            lat=d['lat'],
            long=d['long'],
            short_name=d['short_name'],
            st=d['st'],
            zip=d['zip'],
        )
        results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(dealer_id):
    """Return a single CarDealer by ID."""
    dealers = _load_dealerships()
    for d in dealers:
        if d['id'] == dealer_id:
            return CarDealer(
                address=d['address'],
                city=d['city'],
                full_name=d['full_name'],
                id=d['id'],
                lat=d['lat'],
                long=d['long'],
                short_name=d['short_name'],
                st=d['st'],
                zip=d['zip'],
            )
    return None


def get_dealer_reviews_from_cf(url=None, dealerId=None):
    """Return reviews for a dealer as DealerReview objects."""
    results = []
    reviews = _load_reviews()
    for r in reviews:
        if dealerId is not None and r.get('dealership') != dealerId:
            continue
        sentiment = analyze_review_sentiments(r.get('review', ''))
        review_obj = DealerReview(
            dealership=r.get('dealership'),
            name=r.get('name', ''),
            purchase=r.get('purchase', False),
            review=r.get('review', ''),
            purchase_date=r.get('purchase_date', ''),
            car_make=r.get('car_make', ''),
            car_model=r.get('car_model', ''),
            car_year=r.get('car_year', ''),
            sentiment=sentiment,
            id=r.get('id'),
        )
        results.append(review_obj)
    return results


def analyze_review_sentiments(review_text):
    """
    Simple rule-based sentiment analysis (no Watson API key needed).
    Returns 'positive', 'negative', or 'neutral'.
    """
    if not review_text:
        return 'neutral'
    text_lower = review_text.lower()
    positive_words = [
        'fantastic', 'great', 'excellent', 'good', 'amazing', 'wonderful',
        'best', 'love', 'perfect', 'happy', 'satisfied', 'awesome', 'nice',
        'superb', 'outstanding', 'brilliant', 'friendly', 'helpful',
    ]
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'poor', 'hate',
        'disappointed', 'disappointing', 'rude', 'slow', 'broken', 'defective',
        'useless', 'waste', 'scam', 'fraud', 'never', 'avoid',
    ]
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    if pos_count > neg_count:
        return 'positive'
    elif neg_count > pos_count:
        return 'negative'
    return 'neutral'


def get_request(url, **kwargs):
    """Generic HTTP GET helper (kept for compatibility)."""
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        return json.loads(response.text)
    except Exception as e:
        print(f"Network exception: {e}")
        return {}


def post_request(url, json_payload, **kwargs):
    """Generic HTTP POST helper."""
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        return response
    except Exception as e:
        print(f"Network exception: {e}")
        return None
