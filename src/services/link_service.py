from infrastructure.repositories.link_repository import LinkRepository
from models.schemas import LinkCreate, LinkUpdate


class LinkService:
    def __init__(self, link_repo: LinkRepository):
        self.link_repo = link_repo

    async def get_link(self, link_id):
        return await self.link_repo.get(id=link_id)

    async def get_links(self, limit, offset):
        return await self.link_repo.get_multi(limit=limit, offset=offset)

    async def create_link(self, link_data: LinkCreate):
        return await self.link_repo.create(obj_in=link_data)

    async def create_links(self, links: list[LinkCreate]):
        return await self.link_repo.create_multi(obj_list=links)

    async def update_link(self, link_id: int, link_data: LinkUpdate):
        return await self.link_repo.update(obj_id=link_id, obj_in=link_data)

    async def delete_link(self, link_id: int):
        return await self.link_repo.delete(obj_id=link_id)
