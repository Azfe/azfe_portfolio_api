from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings.
    Las variables se cargan automáticamente desde .env
    """
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # MongoDB - IMPORTANTE: usar nombre del servicio en Docker
    MONGODB_URL: str = "mongodb://mongodb:27017"  # 'mongodb' es el nombre del servicio
    MONGODB_DB_NAME: str = "portfolio_db"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:4321,http://localhost:3000"
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def cors_methods_list(self) -> List[str]:
        return [method.strip() for method in self.CORS_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> List[str]:
        return [header.strip() for header in self.CORS_HEADERS.split(",")]

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AZFE Portfolio API"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
   
          
    class Config:
        env_file = ".env.development"  # Archivo por defecto en desarrollo
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la configuración (cached).
    lru_cache asegura que solo se carga una vez.
    """
    return Settings()


# Instancia global de settings
settings = get_settings()