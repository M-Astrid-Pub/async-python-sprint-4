import inject
from fastapi import FastAPI

from infrastructure.db import engine
from infrastructure.repositories.link_repository import link_crud
from routers.link_router import router as link_router
from routers.link_router import exceptions_map as link_exceptions

from services.link_service import LinkService
from settings import app_settings
from utils.ip_block_middleware import BlacklistMiddleware
from utils.logger import log_handler
import logging

logging.basicConfig(handlers=[log_handler], level=app_settings.APP_LOG_LEVEL)


# Инициализация объекта приложения
app = FastAPI()
app.include_router(link_router)
# Обработчики исключений
for exc, response in link_exceptions.items():
    app.add_exception_handler(exc, lambda req, _: response.to_orjson())

# Прослойка для бана по ip
app.add_middleware(BlacklistMiddleware, blacklist=app_settings.BLACKLIST)

# Инициализация сервиса
service = LinkService(link_crud)


def config(binder: inject.Binder) -> None:
    binder.bind(LinkService, service)


@app.on_event("startup")
async def startup_event():
    inject.configure(config, bind_in_runtime=False)


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down...")
    await engine.dispose()
