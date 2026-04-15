from os import path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    entrypoint: str = "main:app"
    
class ApiConfig(BaseModel):
    prefix: str = "/api"
    message: str = "Welcome to DnD Character Manager API"
    
class CORSConfig(BaseModel):
    origins: list = ["*"]
    methods: list = ["*"]
    headers: list = ["*"]
    credentials: bool = True


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    cors: CORSConfig = CORSConfig()

    POSTGRES_PORT: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_SERVICE: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    @property
    def in_container(self) -> bool:
        return path.exists("/.dockerenv")
    
    @property
    def database_url(self) -> str:
        if self.in_container:
            path = self.POSTGRES_SERVICE
        else:
            path = self.POSTGRES_HOST + ":" + self.POSTGRES_PORT
        
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{path}/{self.POSTGRES_DB}"

settings = Settings()
    