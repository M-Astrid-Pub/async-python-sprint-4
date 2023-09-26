import asyncio
from typing import AsyncGenerator

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.repositories.link_repository import LinkRepository
from main import app
from models import Link
from models.base import metadata
from models.enums import Envs
from models.schemas import LinkCreate, LinkUpdate
from routers.link_router import get_service
from services.link_service import LinkService
from settings import app_settings


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


engine_test = create_async_engine(
    app_settings.get_pg_url(env=Envs.TEST), echo=True, future=True
)
async_session = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def get_dummy_service() -> LinkService:
    return LinkService(LinkRepository(Link, async_session))


app.dependency_overrides[get_service] = get_dummy_service


@pytest.fixture(scope="session")
async def prepare_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="module")
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest.fixture(scope="module")
async def dummy_link_update() -> LinkUpdate:
    return LinkUpdate(
        url_full="http://url-full0", url_short="http://url-short0"
    )


@pytest.fixture(scope="module")
async def dummy_link_create() -> LinkCreate:
    return LinkCreate(
        url_full="http://url-full1", url_short="http://url-short1"
    )


@pytest.fixture(scope="module")
async def dummy_links_multi_create() -> list[LinkCreate]:
    return [
        LinkCreate(url_full="http://url-full2", url_short="http://url-short2"),
        LinkCreate(url_full="http://url-full3", url_short="http://url-short3"),
        LinkCreate(url_full="http://url-full4", url_short="http://url-short4"),
    ]
