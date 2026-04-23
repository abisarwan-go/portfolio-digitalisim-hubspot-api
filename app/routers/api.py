from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException

from app.services.extract_service import ExtractService
from app.services.load_service import LoadService
from app.services.summary_service import SummaryService
from app.services.transform_service import TransformService

router = APIRouter(prefix="/api", tags=["hubspot"])


def _handle_error(exc: Exception) -> HTTPException:
    if isinstance(exc, httpx.HTTPStatusError):
        detail = exc.response.text
        return HTTPException(
            status_code=exc.response.status_code,
            detail=f"HubSpot API error: {detail}",
        )
    if isinstance(exc, httpx.HTTPError):
        return HTTPException(status_code=502, detail=f"HubSpot connection error: {exc}")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=500, detail=str(exc))
    return HTTPException(status_code=500, detail="Unexpected server error")


def _get_services() -> tuple[ExtractService, TransformService, LoadService, SummaryService]:
    return ExtractService(), TransformService(), LoadService(), SummaryService()


@router.get("/contacts")
def get_contacts() -> list[dict]:
    try:
        extract_service, transform_service, load_service, _ = _get_services()
        raw_contacts = extract_service.extract_contacts()
        contacts = transform_service.transform_contacts(raw_contacts)
        load_service.export_raw("contacts", raw_contacts)
        load_service.export_processed("contacts", contacts)
        return contacts
    except Exception as exc:
        raise _handle_error(exc) from exc


@router.get("/companies")
def get_companies() -> list[dict]:
    try:
        extract_service, transform_service, load_service, _ = _get_services()
        raw_companies = extract_service.extract_companies()
        companies = transform_service.transform_companies(raw_companies)
        load_service.export_raw("companies", raw_companies)
        load_service.export_processed("companies", companies)
        return companies
    except Exception as exc:
        raise _handle_error(exc) from exc


@router.get("/deals")
def get_deals() -> list[dict]:
    try:
        extract_service, transform_service, load_service, _ = _get_services()
        raw_deals = extract_service.extract_deals()
        deals = transform_service.transform_deals(raw_deals)
        load_service.export_raw("deals", raw_deals)
        load_service.export_processed("deals", deals)
        return deals
    except Exception as exc:
        raise _handle_error(exc) from exc


@router.get("/summary")
def get_summary() -> dict:
    try:
        extract_service, transform_service, _, summary_service = _get_services()
        contacts = transform_service.transform_contacts(extract_service.extract_contacts())
        companies = transform_service.transform_companies(
            extract_service.extract_companies()
        )
        deals = transform_service.transform_deals(extract_service.extract_deals())
        return summary_service.build_summary(contacts, companies, deals)
    except Exception as exc:
        raise _handle_error(exc) from exc

