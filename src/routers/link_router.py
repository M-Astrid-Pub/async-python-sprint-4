import inject as inject
from fastapi import APIRouter, Depends, Query
from fastapi.responses import ORJSONResponse

from exceptions import ObjectNotFoundException
from models.schemas import (
    LinkCreate,
    LinkUpdate,
    MultipleResponse,
    LinkResponse,
)
from services.link_service import LinkService
from utils.exceptions_handler import ErrorResponse, mapping_to_doc

router = APIRouter(prefix="/links")


async def get_service() -> LinkService:
    return inject.instance(LinkService)


exceptions_map = {
    ObjectNotFoundException: ErrorResponse(
        status_code=404, content="Not found"
    ),
}


@router.get(
    "",
    response_model=MultipleResponse,
    responses=mapping_to_doc(exceptions_map),
)
async def get_links(
    limit: int = Query(default=40, gt=0, le=100),
    offset: int = Query(default=0, ge=0, le=2**32 - 1),
    service: LinkService = Depends(get_service),
) -> ORJSONResponse:
    links = await service.get_links(limit=limit, offset=offset)
    return ORJSONResponse(
        status_code=200,
        content=MultipleResponse.from_entity_list(links),
    )


@router.get(
    "/{link_id}",
    response_model=LinkResponse,
    responses=mapping_to_doc(exceptions_map),
)
async def get_link(
    link_id: int, service: LinkService = Depends(get_service)
) -> ORJSONResponse:
    link = await service.get_link(link_id)
    return ORJSONResponse(
        status_code=200,
        content=LinkResponse.from_entity(link),
    )


@router.post(
    "", response_model=LinkResponse, responses=mapping_to_doc(exceptions_map)
)
async def create_link(
    link_data: LinkCreate, service: LinkService = Depends(get_service)
) -> ORJSONResponse:
    link = await service.create_link(link_data)
    return ORJSONResponse(
        status_code=200,
        content=LinkResponse.from_entity(link),
    )


@router.put(
    "/{link_id}",
    response_model=LinkResponse,
    responses=mapping_to_doc(exceptions_map),
)
async def update_link(
    link_id: int,
    link_data: LinkUpdate,
    service: LinkService = Depends(get_service),
) -> ORJSONResponse:
    link = await service.update_link(link_id, link_data)
    return ORJSONResponse(
        status_code=200,
        content=LinkResponse.from_entity(link),
    )


@router.delete("/{link_id}", responses=mapping_to_doc(exceptions_map))
async def delete_link(
    link_id: int, service: LinkService = Depends(get_service)
) -> ORJSONResponse:
    await service.delete_link(link_id)
    return ORJSONResponse(
        status_code=200,
        content="OK",
    )


@router.post("/multi-create", responses=mapping_to_doc(exceptions_map))
async def multi_create_links(
    links: list[LinkCreate], service: LinkService = Depends(get_service)
) -> ORJSONResponse:
    await service.create_links(links)
    return ORJSONResponse(
        status_code=200,
        content="OK",
    )
