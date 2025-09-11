from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "RenewMart API"
    debug: bool = True
    database_url: str = "postgresql://postgres:RenewMart_Password@localhost:5432/renewmart_db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = None  # Disable .env file loading

settings = Settings()
