from __future__ import annotations

from typing import Any

import httpx

from app.config import get_settings


class HubSpotClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.hubspot_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.hubspot_access_token}",
            "Content-Type": "application/json",
        }

    def _request(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = httpx.get(url, headers=self.headers, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()

    def get_object_page(
        self,
        object_name: str,
        properties: list[str],
        after: str | None = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "properties": ",".join(properties),
            "limit": limit,
        }
        if after:
            params["after"] = after
        return self._request(f"/crm/v3/objects/{object_name}", params)

    def get_all_objects(
        self, object_name: str, properties: list[str], limit: int = 100
    ) -> list[dict[str, Any]]:
        all_results: list[dict[str, Any]] = []
        after: str | None = None

        while True:
            payload = self.get_object_page(
                object_name=object_name,
                properties=properties,
                after=after,
                limit=limit,
            )
            all_results.extend(payload.get("results", []))
            paging = payload.get("paging", {})
            next_data = paging.get("next")
            if not next_data:
                break
            after = str(next_data.get("after"))
            if not after:
                break

        return all_results

