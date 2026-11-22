from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Bluesky
    bluesky_handle: str | None = None
    bluesky_app_password: str | None = None
    
    # Blogger
    blogger_client_id: str | None = None
    blogger_client_secret: str | None = None
    blogger_refresh_token: str | None = None
    blogger_blog_id: str | None = None

    # Discord
    discord_webhook_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()