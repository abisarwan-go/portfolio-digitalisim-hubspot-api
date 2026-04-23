from __future__ import annotations

from app.clients.hubspot_client import HubSpotClient
from app.config import get_settings


CONTACT_PROPERTIES = ["firstname", "lastname", "email", "phone"]
COMPANY_PROPERTIES = ["name", "domain", "industry", "phone"]
DEAL_PROPERTIES = ["dealname", "amount", "dealstage", "pipeline", "closedate"]


class ExtractService:
    def __init__(self, client: HubSpotClient | None = None) -> None:
        self.client = client or HubSpotClient()

    def extract_contacts(self) -> list[dict]:
        settings = get_settings()
        return self.client.get_all_objects(
            "contacts", properties=CONTACT_PROPERTIES, limit=settings.page_size
        )

    def extract_companies(self) -> list[dict]:
        settings = get_settings()
        return self.client.get_all_objects(
            "companies", properties=COMPANY_PROPERTIES, limit=settings.page_size
        )

    def extract_deals(self) -> list[dict]:
        settings = get_settings()
        return self.client.get_all_objects(
            "deals", properties=DEAL_PROPERTIES, limit=settings.page_size
        )

