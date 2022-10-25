from pydantic import (
    BaseSettings,
    Field
)
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_PASS: str = Field(env='DB_PASS', default='postgres')
    DB_USER: str = Field(env='DB_USER', default='postgres')
    DB_NAME: str = Field(env='DB_NAME', default='postgres')
    DB_HOST: str = Field(env='DB_HOST', default='localhost')
    DB_PORT: str = Field(env='DB_PORT', default=5432)

    JWT_KEY: str = Field(env='JWT_KEY')
    JWT_ALGORITHM: str = Field(env='JWT_ALGORITHM', default='HS256')
    ACCESS_TOKEN_LIFETIME_MINUTES: str = Field(env='ACCESS_TOKEN_LIFETIME_MINUTES', default=480)

    ADMIN_ACTIVATION_CODE: str = Field(env='ADMIN_ACTIVATION_CODE')


settings = Settings().dict()
