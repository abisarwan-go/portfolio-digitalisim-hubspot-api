from __future__ import annotations

from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers.api import router as api_router
from app.services.extract_service import ExtractService
from app.services.summary_service import SummaryService
from app.services.transform_service import TransformService

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="HubSpot ETL Portfolio", version="0.1.0")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    try:
        extract_service = ExtractService()
        transform_service = TransformService()
        summary_service = SummaryService()
        contacts = transform_service.transform_contacts(extract_service.extract_contacts())
        companies = transform_service.transform_companies(
            extract_service.extract_companies()
        )
        deals = transform_service.transform_deals(extract_service.extract_deals())
        summary = summary_service.build_summary(contacts, companies, deals)
    except (httpx.HTTPError, ValueError):
        contacts = []
        companies = []
        deals = []
        summary = {
            "total_contacts": 0,
            "total_companies": 0,
            "total_deals": 0,
            "total_deals_amount": 0,
        }

    context = {
        "request": request,
        "summary": summary,
        "contacts_preview": contacts[:5],
        "companies_preview": companies[:5],
        "deals_preview": deals[:5],
    }
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )
