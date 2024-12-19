from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = "KONFIO"
    DB_PORT: int = 3306
    DB_URL: str = Field(..., env="DB_URL")
    LOCALSTACK_URL: str = Field(..., env="LOCALSTACK_URL")
    EVENT_BUCKET_NAME: str = Field(..., env="EVENT_BUCKET_NAME")
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(..., env="AWS_REGION")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
