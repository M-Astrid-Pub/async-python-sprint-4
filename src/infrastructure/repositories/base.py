from typing import TypeVar

from pydantic import BaseModel

from exceptions import ObjectNotFoundException
from models.base import Base
from typing import Any, Dict, Generic, List, Optional, Type, Union
from sqlalchemy import select, over, func, update, delete
from fastapi.encoders import jsonable_encoder


class Repository:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryDB(
    Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(
        self, model: Type[ModelType], session_maker: callable
    ) -> None:
        self._model = model
        self._session_maker = session_maker

    async def get(self, id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == id)
        async with self._session_maker() as db:
            results = await db.execute(statement=statement)
        if not (res := results.scalar_one_or_none()):
            raise ObjectNotFoundException
        return res

    async def get_multi(
        self, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = (
            select(
                self._model,
                over(func.count()).label("total"),
            )
            .offset(offset)
            .limit(limit)
        )
        async with self._session_maker() as db:
            results = await db.execute(statement=statement)
        return results.all()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        async with self._session_maker() as db:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, obj_id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        stmt = update(self._model).where(self._model.id == obj_id).values(**obj_in_data).returning(
            self._model
        )
        async with self._session_maker() as db:
            if not (db_obj := (await db.execute(statement=stmt)).one_or_none()):
                raise ObjectNotFoundException
            await db.commit()
        return db_obj

    async def delete(self, *, obj_id: int) -> None:
        stmt = delete(self._model).where(self._model.id == obj_id).returning(self._model.id)
        async with self._session_maker() as db:
            if not (db_obj := (await db.execute(statement=stmt)).one_or_none()):
                raise ObjectNotFoundException
            await db.commit()

    async def create_multi(self, *, obj_list: list[CreateSchemaType]) -> None:
        model_objects = [
            self._model(**jsonable_encoder(obj_in)) for obj_in in obj_list
        ]
        async with self._session_maker() as db:
            db.add_all(model_objects)
            await db.commit()
