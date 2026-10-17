# IBM Full Stack Cloud Development Capstone Project

## Project Name: Best Cars Dealership

A full-stack web application built with **Django** (Python) and **React** as part of the IBM Full Stack Software Developer Professional Certificate capstone.

## Project Overview

Best Cars Dealership is an online platform where users can:
- Browse car dealerships across the United States
- Filter dealerships by state
- View detailed dealer information and customer reviews
- Post reviews for dealerships (after logging in)
- Register and log in with user accounts

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Python 3.11 |
| Frontend | HTML5, Bootstrap 4, Django Templates |
| Database | SQLite (development), PostgreSQL (production) |
| APIs | Django REST views (dealer/review data from JSON) |
| CI/CD | GitHub Actions |
| Deployment | IBM Cloud / Render |
| Sentiment Analysis | Rule-based NLP |

## Project Structure

```
server/
├── djangobackend/      # Django project settings
├── djangoapp/          # Main application
│   ├── models.py       # CarMake, CarModel, CarDealer, DealerReview
│   ├── views.py        # All view functions + JSON API endpoints
│   ├── restapis.py     # Data access layer
│   ├── urls.py         # URL routing
│   └── templates/      # HTML templates
cloudant/
└── data/               # JSON data files (dealerships, reviews)
.github/
└── workflows/          # GitHub Actions CI/CD
```

## Key Features

- **Dynamic dealer listings** with state-based filtering
- **Dealer reviews** with sentiment analysis (positive/negative/neutral)
- **User authentication** — register, login, logout
- **Admin panel** — manage CarMake and CarModel entries
- **JSON API endpoints** — `/djangoapp/api/dealers/`, `/djangoapp/api/reviews/dealer/<id>/`
- **CI/CD pipeline** via GitHub Actions (lint + test on every push)

## Setup & Run Locally

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://127.0.0.1:8000/djangoapp/

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /djangoapp/api/dealers/` | All dealers |
| `GET /djangoapp/api/dealers/?state=KS` | Dealers by state |
| `GET /djangoapp/api/dealers/<id>/` | Dealer by ID |
| `GET /djangoapp/api/reviews/dealer/<id>/` | Reviews for a dealer |
| `GET /djangoapp/api/carmakes/` | All car makes and models |
| `GET /djangoapp/api/sentiment/?text=Fantastic+services` | Sentiment analysis |

## Author

IBM Full Stack Software Developer Capstone Project  
© 2024 Best Cars Dealership
