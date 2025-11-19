from functools import lru_cache
from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    env: str = Field(default="development")

    google_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    google_project_id: str = Field(..., alias="GOOGLE_PROJECT_ID")
    gemini_model_name: str = Field("gemini-1.5-flash", alias="GEMINI_MODEL_NAME")

    langchain_api_key: str | None = Field(None, alias="LANGCHAIN_API_KEY")
    langsmith_api_key: str = Field(..., alias="LANGSMITH_API_KEY")
    langsmith_project: str = Field(..., alias="LANGSMITH_PROJECT")

    mongo_uri: str | None = Field(None, alias="MONGO_URI")
    redis_url: str | None = Field(None, alias="REDIS_URL")

    gmail_client_id: str = Field(..., alias="GMAIL_CLIENT_ID")
    gmail_client_secret: str = Field(..., alias="GMAIL_CLIENT_SECRET")
    gmail_refresh_token: str = Field(..., alias="GMAIL_REFRESH_TOKEN")
    email_sender: str = Field(..., alias="EMAIL_SENDER")

    app_base_url: HttpUrl = Field(..., alias="APP_BASE_URL")

    rate_limit_default: str = Field("60/minute", alias="RATE_LIMIT_DEFAULT")
    log_level: str = Field("INFO", alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
