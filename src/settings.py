from functools import lru_cache
from pydantic import (
    BaseSettings,
    Field
)
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # DB_PASS: str = Field(env='DB_PASS', default='postgres')
    # DB_USER: str = Field(env='DB_USER', default='postgres')
    # DB_NAME: str = Field(env='DB_NAME', default='postgres')
    # DB_HOST: str = Field(env='DB_HOST', default='localhost')
    # DB_PORT: str = Field(env='DB_PORT', default=5432)
    #
    # JWT_KEY: str = Field(env='JWT_KEY')
    # JWT_ALGORITHM: str = Field(env='JWT_ALGORITHM', default='HS256')
    # ACCESS_TOKEN_LIFETIME_MINUTES: str = Field(env='ACCESS_TOKEN_LIFETIME_MINUTES', default=480)
    #
    # ADMIN_ACTIVATION_CODE: str = Field(env='ADMIN_ACTIVATION_CODE')
    #
    # CLICKHOUSE_DB: str = Field(env='CLICKHOUSE_DB')
    # CLICKHOUSE_ADV_TABLE: str = Field(env='CLICKHOUSE_ADV_TABLE')
    # COLLECT_CLICKHOUSE_DATA: str = Field(env='COLLECT_CLICKHOUSE_DATA')
    #
    # MONGODB_USER: str = Field(env='MONGODB_USER')
    # MONGODB_PASSWORD: str = Field(env='MONGODB_PASSWORD')
    # MONGODB_HOST: str = Field(env='MONGODB_HOST')
    # MONGODB_PORT: str = Field(env='MONGODB_PORT')

    DB_PASS: str
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    JWT_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_MINUTES: str

    ADMIN_ACTIVATION_CODE: str

    CLICKHOUSE_DB: str
    CLICKHOUSE_ADV_TABLE: str
    COLLECT_CLICKHOUSE_DATA: str

    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: str

    class Config:
        env_file = '.env'


# settings = Settings().dict()


@lru_cache()
def configure_settings():
    return Settings()


settings = configure_settings()
