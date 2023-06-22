from pydantic import BaseSettings
import cloudinary


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"

    cloud_name: str = "cloudinary name"
    cloud_api_key: str = "000000000000000000"
    cloud_api_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def config_cloudinary():
    return cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.cloud_api_key,
        api_secret=settings.cloud_api_secret,
        secure=True
    )


settings = Settings()
