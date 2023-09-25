from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator

from models import Link


class LinkUpdate(BaseModel):
    url_full: str
    url_short: str

    @field_validator("url_full", "url_short")
    @classmethod
    def check_url(cls, val: str) -> str:
        result = urlparse(val)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Not a valid url.")
        return val

    class Config:
        str_strip_whitespace = True


class LinkCreate(LinkUpdate):
    pass


@dataclass
class LinkResponse:
    id: int
    url_full: str
    url_short: str
    created_at: datetime

    @classmethod
    def from_entity(cls, data: Link):
        return cls(
            id=data.id,
            url_full=data.url_full,
            url_short=data.url_short,
            created_at=data.created_at,
        )


@dataclass
class MultipleResponse:
    total: int
    items: list[LinkResponse]

    @classmethod
    def from_entity_list(cls, data: list[tuple[Link, int]]):
        if len(data) == 0:
            return cls(total=0, items=[])
        return cls(
            total=data[0][1],
            items=[LinkResponse.from_entity(row[0]) for row in data],
        )
