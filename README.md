# Name Classifier API v2

A Django REST API that classifies a name using Genderize, Agify, and Nationalize APIs and returns a processed response.

Built for **Backend Wizards — Stage 0 Assessment**.

---

## Live API

Base URL:

https://name-classifier-api-v2.vercel.app

Endpoints:

POST /api/profiles/ (create profile with name)

GET /api/profiles (list profiles)

GET /api/profiles/{id} (get profile by id)

DELETE /api/profiles/{id}/delete (delete profile)

Example request:

POST /api/profiles/

Body: {"name": "john"}

---

## What the API Does

* Accepts a `name` in POST request body
* Calls Genderize API for gender data
* Calls Agify API for age data
* Calls Nationalize API for country data
* Extracts:

  * gender
  * gender_probability
  * sample_size (count)
  * age
  * age_group (computed from age)
  * country_id
  * country_probability
* Stores the profile in database
* Returns the profile data

---

## Success Response

```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "john",
    "gender": "male",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 30,
    "age_group": "adult",
    "country_id": "US",
    "country_probability": 0.15,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

---

## Error Format

```json
{
  "status": "error",
  "message": "<error message>"
}
```

---

## Tech Stack

* Python
* Django
* Django REST Framework
* Requests
* Mangum
* Vercel (Deployment)

---

## Run Locally

Clone repo:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Run server:

python manage.py runserver

Test:

POST to http://localhost:8000/api/profiles/ with body {"name": "john"}

---

## Author

Name: [Your Name]
Email: [your.email@example.com]
Stack: Django