from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("AK01_ENV", "dev")
    database_url: str = os.getenv("AK01_DATABASE_URL", "sqlite+pysqlite:///:memory:")
    log_level: str = os.getenv("AK01_LOG_LEVEL", "INFO")
    external_models_allowed: bool = os.getenv("AK01_EXTERNAL_MODELS_ALLOWED", "false").lower() == "true"


settings = Settings()
