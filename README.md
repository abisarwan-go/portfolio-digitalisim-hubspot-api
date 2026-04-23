# HubSpot ETL Pipeline - V1 Portfolio

Mini platform data autour de HubSpot, construite pour montrer une stack Python orientee
API REST, ETL, Docker et logique CRM.

## Stack

- Python 3.12
- FastAPI
- httpx
- python-dotenv
- Jinja2
- uv

## Structure

```text
hubspot-etl-pipeline/
├── .env.example
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── data/
│   ├── raw/
│   └── processed/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── clients/hubspot_client.py
│   ├── routers/api.py
│   ├── services/
│   │   ├── extract_service.py
│   │   ├── transform_service.py
│   │   ├── load_service.py
│   │   └── summary_service.py
│   ├── templates/index.html
│   └── static/style.css
└── tests/
```

## Configuration

1. Copier le fichier d'environnement:

```bash
cp .env.example .env
```

2. Remplir `HUBSPOT_ACCESS_TOKEN` dans `.env`.

## Installation et lancement (uv)

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Application: `http://127.0.0.1:8000`

## Endpoints V1

- `GET /api/contacts`
- `GET /api/companies`
- `GET /api/deals`
- `GET /api/summary`
- `GET /`

## Notes V1

- Le token HubSpot reste uniquement cote backend.
- Les exports CSV sont ecrits dans `data/raw` et `data/processed`.
- OAuth est volontairement hors scope pour cette V1.

