import httpx
from fastapi.encoders import jsonable_encoder
from starlette import status

from main import app
from models.schemas import LinkCreate, LinkUpdate


async def test_create_link(
        client: httpx.AsyncClient, dummy_link_create: LinkCreate, prepare_db
) -> None:
    link_data = jsonable_encoder(dummy_link_create)
    result = await client.post(app.url_path_for("create_link"), json=link_data)
    assert result.status_code == status.HTTP_200_OK

    item = result.json()
    for key, val in jsonable_encoder(dummy_link_create).items():
        assert item[key] == val

    result = await client.get(app.url_path_for("get_link", link_id=item["id"]))
    assert result.status_code == status.HTTP_200_OK
    assert result.json() == item


async def test_update_link(
        client: httpx.AsyncClient, dummy_link_update: LinkUpdate
) -> None:
    link_id = (await client.get(app.url_path_for("get_links"))).json()["items"][0]["id"]

    link_data = jsonable_encoder(dummy_link_update)
    result = await client.put(app.url_path_for("update_link", link_id=link_id), json=link_data)
    assert result.status_code == status.HTTP_200_OK

    item = result.json()
    for key, val in jsonable_encoder(dummy_link_update).items():
        assert item[key] == val

    result = await client.get(app.url_path_for("get_link", link_id=item["id"]))
    assert result.status_code == status.HTTP_200_OK
    assert result.json() == item


async def test_delete_link(client: httpx.AsyncClient) -> None:
    link_data = (await client.get(app.url_path_for("get_links"))).json()["items"][0]

    result = await client.delete(app.url_path_for("delete_link", link_id=link_data["id"]))
    assert result.status_code == status.HTTP_200_OK

    result = await client.get(app.url_path_for("get_link", link_id=link_data["id"]))
    assert result.status_code == status.HTTP_404_NOT_FOUND


async def test_multi_create_link(
        client: httpx.AsyncClient, dummy_links_multi_create: list[LinkCreate]
) -> None:
    result = await client.get(app.url_path_for("get_links"))
    assert result.status_code == status.HTTP_200_OK
    init_count = result.json()["total"]

    result = await client.post(
        app.url_path_for("multi_create_links"), json=jsonable_encoder(dummy_links_multi_create)
    )
    assert result.status_code == status.HTTP_200_OK

    result = await client.get(app.url_path_for("get_links"))
    post_count = result.json()["total"]

    assert init_count + len(dummy_links_multi_create) == post_count
