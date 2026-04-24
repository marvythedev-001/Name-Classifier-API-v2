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

## Deploying with Supabase (Postgres)

This project supports Postgres via `DATABASE_URL`. Supabase is a good hosted Postgres option.

1. Create a project on Supabase (https://supabase.com) and note the Database connection string.

2. In your Supabase project dashboard: Settings → Database → Connection string → copy the `Connection string` (example: `postgres://USER:PASS@HOST:PORT/DBNAME`).

3. In your Vercel project settings, add the following Environment Variables:

- `DATABASE_URL` = (the Supabase connection string)
- `SECRET_KEY` = (your Django secret key)
- `DEBUG` = `False`

4. Run migrations locally (or from a machine that has `DATABASE_URL` set to Supabase) to create tables:

```bash
pip install -r requirements.txt
export DATABASE_URL="postgres://USER:PASS@HOST:PORT/DBNAME"
python manage.py migrate
```

On Windows (PowerShell):

```powershell
$Env:DATABASE_URL = "postgres://USER:PASS@HOST:PORT/DBNAME"
python manage.py migrate
```

5. Deploy to Vercel. The app will use `DATABASE_URL` in production and fall back to SQLite locally.

Notes:
- Do not store secrets in `vercel.json`; use the Vercel Dashboard for env variables.
- You can also use Supabase's SQL editor to run migrations if you prefer.

## Vercel Deployment Files

The following files are configured for Vercel deployment:

- `vercel.json` - Vercel configuration with Python runtime and routing
- `runtime.txt` - Specifies Python 3.12
- `requirements.txt` - All Python dependencies including PostgreSQL support
- `.vercelignore` - Excludes unnecessary files from deployment

## Deploy Steps

1. Install Vercel CLI: `npm install -g vercel`
2. Login to Vercel: `vercel login`
3. Deploy: `vercel --prod` (or run the `vercel-deploy.sh` script)
4. Set environment variables in Vercel dashboard as described above



Parser Design Decisions
Rule-based parsing ensures deterministic behavior.
No AI inference is used.
Parsing output reuses the main filtering engine.
Prevents duplicated query logic.
Keeps implementation fast and predictable.
Limitations of the Parser

The parser intentionally keeps scope limited.

Current limitations include:

Only predefined countries are supported.
No spelling correction.
Cannot interpret complex grammar.
No synonym detection (e.g., "guys", "ladies").
Does not support multiple conflicting constraints.
English language only.
Cannot interpret statistical or comparative queries.

These constraints were accepted to maintain rule-based determinism and predictable performance.

Performance Considerations
Filtering executed at database level.
Sorting performed via SQL ORDER BY.
Pagination applied before serialization.
Unique constraint prevents duplicate seed inserts.
Avoids unnecessary full-table scans.

## Author

Name: [Your Name]
Email: [your.email@example.com]
Stack: Django