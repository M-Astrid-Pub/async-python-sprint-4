from pydantic_settings import BaseSettings

from models.enums import Envs


class Settings(BaseSettings):
    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    BLACKLIST: list[str]
    PG_TEST_DB: str = "links_test"
    APP_LOG_LEVEL: str = "DEBUG"
    ENABLE_LOG_FORMATTER: bool = True

    class Config:
        env_file = ".env"

    def get_pg_url(self, env: Envs = Envs.PROD):
        if env == Envs.PROD:
            db_name = self.PG_DB
        else:
            db_name = self.PG_TEST_DB
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{db_name}"


app_settings = Settings()
