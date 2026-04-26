from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación.
    Las variables se cargan automáticamente desde archivos .env
    """

    # Environment
    ENVIRONMENT: str = Field(
        default="development", description="Environment: development, test, production"
    )

    # Server
    HOST: str = Field(default="0.0.0.0", alias="API_HOST")
    PORT: int = Field(default=8000, alias="API_PORT")

    @property
    def DEBUG(self) -> bool:
        """Debug mode enabled for development and test environments"""
        return self.ENVIRONMENT in ["development", "test"]

    # MongoDB
    MONGODB_URL: str = Field(default="mongodb://localhost:27017")
    MONGODB_DB_NAME: str = Field(default="portfolio_db", alias="DATABASE_NAME")

    # CORS
    CORS_ORIGINS: str = "http://localhost:4321,http://localhost:3000"
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def cors_methods_list(self) -> list[str]:
        return [method.strip() for method in self.CORS_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> list[str]:
        return [header.strip() for header in self.CORS_HEADERS.split(",")]

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = Field(default="AZFE Portfolio API", alias="api_title")
    VERSION: str = Field(default="1.0.0", alias="api_version")

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Email / Notifications
    EMAIL_ENABLED: bool = Field(default=False)
    SENDGRID_API_KEY: str = Field(default="")
    SMTP_FROM: str = Field(default="")
    NOTIFICATION_EMAIL_TO: str = Field(default="alexzapata1984@gmail.com")

    # Deprecated SMTP settings — kept for backward compatibility
    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_USE_TLS: bool = Field(default=True)

    model_config = SettingsConfigDict(
        env_file=".env.development.local",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene la configuración (cached).
    lru_cache asegura que solo se carga una vez.
    """
    return Settings()


# Instancia global de settings
settings = get_settings()
