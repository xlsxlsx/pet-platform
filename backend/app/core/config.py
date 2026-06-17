from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Pet Platform API"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    cors_allowed_origins: str = "http://127.0.0.1:5173,http://localhost:5173"
    allow_admin_registration: bool = False
    auth_debug_codes: bool = False
    captcha_ttl_seconds: int = 120
    sms_code_ttl_seconds: int = 300
    sms_code_length: int = 6
    sms_provider: str = "local"

    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_database: str = "pet_platform"

    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    @property
    def mysql_async_dsn(self) -> str:
        user = quote_plus(self.mysql_user)
        password = quote_plus(self.mysql_password)
        return (
            f"mysql+aiomysql://{user}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
