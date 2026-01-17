from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str = Field(..., env="MONGODB_URL")
    database_name: str = Field(..., env="DATABASE_NAME")
    
    # API
    api_title: str = "Portfolio API"
    api_version: str = "1.0.0"
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")

    # Extra config
    debug: bool = Field(False, env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
