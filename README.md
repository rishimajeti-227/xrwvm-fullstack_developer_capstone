# xrwvm-fullstack_developer_capstone

## Project Name: fullstack_developer_capstone

A full-stack web application built with **Django** (Python) and **React** as part of the IBM Full Stack Software Developer Professional Certificate capstone.

## Overview

Best Cars Dealership is an online platform where users can browse car dealerships across the United States, view dealer reviews, and post their own reviews after logging in.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Python 3.11 |
| Frontend | HTML5, Bootstrap 4, React |
| Database | SQLite (development) |
| CI/CD | GitHub Actions |
| Sentiment | Rule-based NLP |

## Setup

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /djangoapp/fetchDealers` | All dealers |
| `GET /djangoapp/fetchDealers/Kansas` | Dealers by state |
| `GET /djangoapp/fetchDealer/<id>` | Dealer by ID |
| `GET /djangoapp/fetchReviews/dealer/<id>` | Reviews for dealer |
| `GET /djangoapp/get_cars` | Car makes and models |
| `GET /djangoapp/analyze/<text>` | Sentiment analysis |
| `POST /djangoapp/login` | Login |
| `GET /djangoapp/logout` | Logout |

## Repository

Repository name: xrwvm-fullstack_developer_capstone  
Project name: fullstack_developer_capstone
