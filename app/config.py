from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
try:
    load_dotenv(ROOT_DIR / ".env")
except PermissionError:
    # Fallback for restricted environments: rely on exported env vars.
    pass


@dataclass(frozen=True)
class Settings:
    hubspot_access_token: str
    client_secret: str
    hubspot_base_url: str = "https://api.hubapi.com"
    page_size: int = 100

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("HUBSPOT_ACCESS_TOKEN", "").strip()
        client_secret = os.getenv("CLIENT_SECRET", "").strip()
        if not token:
            raise ValueError("HUBSPOT_ACCESS_TOKEN is missing in .env.")
        if not client_secret:
            raise ValueError("CLIENT_SECRET is missing in .env.")
        return cls(
            hubspot_access_token=token,
            client_secret=client_secret,
            hubspot_base_url=os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com"),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()

