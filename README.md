# Widget App - FastAPI + React (Vite) POC (POC)

A production-ready FastAPI **proof-of-concept** fo Widget Company with PostgreSQL, SQLAlchemy, Vite+React frontend, and clean service-layer pricing logic. Implements basket pricing rules, delivery charges, and a buy-one-get-second-half-price offer. This is just a proof of concept I have made for the demonstration purposes.

## Stack
- Backend: FastAPI, SQLAlchemy, pydantic-settings
- Frontend: Vite + React (JavaScript)
- DB: PostgreSQL (Docker)
- Orchestration: Docker Compose

## Quick start (Docker)
```bash
# from project root
docker compose up -d --build

# seed database (one-time; backend must be healthy)
docker exec -it widget_backend python seed.py
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API base: http://localhost:8000/api/v1

## Local development (without Docker)
1) Start Postgres (or use `docker compose up -d db`)
2) Configure `.env`
```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/widget_db
APP_NAME=Widget API
DEBUG=true
```
3) Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --app-dir .
```
4) Frontend
```bash
cd frontend
npm install
npm run dev
```

## API
- Health: GET `/health`
- Catalogue
  - Products: GET/POST `/api/v1/catalogue/products`, GET/PUT/PATCH/DELETE `/api/v1/catalogue/products/{code}`
  - Delivery rules: GET/POST `/api/v1/catalogue/delivery-rules`, PUT/PATCH/DELETE `/api/v1/catalogue/delivery-rules/{rule_id}`
  - Offers: GET/POST `/api/v1/catalogue/offers`, PUT/PATCH/DELETE `/api/v1/catalogue/offers/{offer_id}`
- Checkout: POST `/api/v1/checkout/total`

## Frontend
- Pages
  - Catalogue management (CRUD for products; lists offers and delivery rules)
  - Checkout (build basket and compute totals)
- Env: `VITE_API_BASE_URL` (docker-compose sets to http://localhost:8000/api/v1)

## Assumptions
These are the assumptions I have made whole building this proof of concept.
- Delivery rules tiers: 0 => 4.95, 50 => 2.95, 90 => 0.0 (largest `min_total <= order_total` wins) (this was given in the document).
- There are some offers already made in the project but if you want to extend the offer like buy one get two free or something like that you can extend via `OfferType` and BasketService.

