from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities import Profile
from app.infrastructure.mappers import ProfileMapper
from app.shared.interfaces.repository import IProfileRepository


class ProfileRepository(IProfileRepository):
    """Concrete implementation of Profile repository using MongoDB."""

    collection_name = "profiles"

    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._collection = db[self.collection_name]
        self._mapper = ProfileMapper()

    async def add(self, entity: Profile) -> Profile:
        doc = self._mapper.to_persistence(entity)
        await self._collection.insert_one(doc)
        return entity

    async def update(self, entity: Profile) -> Profile:
        doc = self._mapper.to_persistence(entity)
        await self._collection.replace_one({"_id": entity.id}, doc)
        return entity

    async def delete(self, entity_id: str) -> bool:
        result = await self._collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def get_by_id(self, entity_id: str) -> Profile | None:
        doc = await self._collection.find_one({"_id": entity_id})
        if doc is None:
            return None
        return self._mapper.to_domain(doc)

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str | None = None,
        ascending: bool = True,
    ) -> list[Profile]:
        cursor = self._collection.find().skip(skip).limit(limit)
        if sort_by:
            cursor = cursor.sort(sort_by, 1 if ascending else -1)
        docs = await cursor.to_list(length=limit)
        return self._mapper.to_domain_list(docs)

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        return await self._collection.count_documents(filters or {})

    async def exists(self, entity_id: str) -> bool:
        count = await self._collection.count_documents({"_id": entity_id})
        return count > 0

    async def find_by(self, **filters: Any) -> list[Profile]:
        docs = await self._collection.find(filters).to_list(length=100)
        return self._mapper.to_domain_list(docs)

    async def get_profile(self) -> Profile | None:
        doc = await self._collection.find_one()
        if doc is None:
            return None
        return self._mapper.to_domain(doc)

    async def profile_exists(self) -> bool:
        count = await self._collection.count_documents({})
        return count > 0
