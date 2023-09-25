from pydantic_settings import BaseSettings


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

    def get_pg_url(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

    def get_test_pg_url(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_TEST_DB}"


app_settings = Settings()
