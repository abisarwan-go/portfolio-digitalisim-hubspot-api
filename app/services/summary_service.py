from __future__ import annotations

from typing import Any


class SummaryService:
    def build_summary(
        self,
        contacts: list[dict[str, Any]],
        companies: list[dict[str, Any]],
        deals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        total_amount = 0.0
        for deal in deals:
            raw_amount = deal.get("amount") or 0
            try:
                total_amount += float(raw_amount)
            except (TypeError, ValueError):
                continue

        return {
            "total_contacts": len(contacts),
            "total_companies": len(companies),
            "total_deals": len(deals),
            "total_deals_amount": round(total_amount, 2),
        }

