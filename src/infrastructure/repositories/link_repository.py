from models.db_models import Link as LinkModel
from models.schemas import LinkCreate, LinkUpdate
from .base import RepositoryDB
from ..db import async_session


class LinkRepository(RepositoryDB[LinkModel, LinkCreate, LinkUpdate]):
    pass


link_crud = LinkRepository(LinkModel, async_session)
