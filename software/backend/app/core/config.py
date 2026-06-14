from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./terrasafe.db"
    cors_origins: str = "http://localhost:5173"

    weather_lat: float = -20.7546
    weather_lng: float = -42.8825
    weather_grid_step: float = 0.05
    weather_cache_ttl_minutes: int = 10
    weather_rain_grid_ttl_minutes: int = 5
    weather_max_rain_mm: float = 50.0

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    model_config = {"env_file": ".env"}


settings = Settings()
