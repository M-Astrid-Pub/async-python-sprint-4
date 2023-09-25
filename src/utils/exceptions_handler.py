from fastapi.responses import ORJSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int
    content: str

    def to_orjson(self):
        return ORJSONResponse(
            status_code=self.status_code,
            content=self.content,
        )


def mapping_to_doc(mapping: dict[Exception, ErrorResponse]):
    return {val.status_code: {"model": val} for val in mapping.values()}
