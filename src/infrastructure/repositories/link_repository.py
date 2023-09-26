from models.db_models import Link
from models.schemas import LinkCreate, LinkUpdate
from .base import RepositoryDB
from ..db import async_session


class LinkRepository(RepositoryDB[Link, LinkCreate, LinkUpdate]):
    pass


link_crud = LinkRepository(Link, async_session)
