from functools import lru_cache
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path

# Load .env from app/.env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)


class Settings(BaseSettings):
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")

    DATABASE_URI: str = ""

    @model_validator(mode='after')
    def set_database_uri(self) -> 'Settings':
        self.DATABASE_URI = (
            f"postgresql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return self

    def __init__(self, **values):
        super().__init__(**values)
        print("\nLoaded settings:")
        for key, value in self.model_dump().items():
            print(f"{key}: {value} ({type(value).__name__})")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
