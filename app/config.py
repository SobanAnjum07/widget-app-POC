from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="Widget API")
    debug: bool = Field(default=True)
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/widget_db",
        alias="DATABASE_URL",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()  # singleton-like import
