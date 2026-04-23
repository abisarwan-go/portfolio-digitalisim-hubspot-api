from __future__ import annotations

from typing import Any


def _normalize_record(record: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    properties = record.get("properties", {})
    normalized = {key: properties.get(key) for key in keys}
    normalized["id"] = record.get("id")
    return normalized


class TransformService:
    def transform_contacts(self, contacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            _normalize_record(contact, ["firstname", "lastname", "email", "phone"])
            for contact in contacts
        ]

    def transform_companies(
        self, companies: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return [
            _normalize_record(company, ["name", "domain", "industry", "phone"])
            for company in companies
        ]

    def transform_deals(self, deals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            _normalize_record(
                deal, ["dealname", "amount", "dealstage", "pipeline", "closedate"]
            )
            for deal in deals
        ]

