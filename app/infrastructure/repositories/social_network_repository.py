from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities import SocialNetwork
from app.infrastructure.mappers import SocialNetworkMapper
from app.shared.interfaces.repository import (
    IOrderedRepository,
    ISocialNetworkRepository,
)


class SocialNetworkRepository(
    ISocialNetworkRepository, IOrderedRepository[SocialNetwork]
):
    """Concrete implementation of SocialNetwork repository using MongoDB."""

    collection_name = "social_networks"

    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._collection = db[self.collection_name]
        self._mapper = SocialNetworkMapper()

    async def add(self, entity: SocialNetwork) -> SocialNetwork:
        doc = self._mapper.to_persistence(entity)
        await self._collection.insert_one(doc)
        return entity

    async def update(self, entity: SocialNetwork) -> SocialNetwork:
        doc = self._mapper.to_persistence(entity)
        await self._collection.replace_one({"_id": entity.id}, doc)
        return entity

    async def delete(self, entity_id: str) -> bool:
        result = await self._collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def get_by_id(self, entity_id: str) -> SocialNetwork | None:
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
    ) -> list[SocialNetwork]:
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

    async def find_by(self, **filters: Any) -> list[SocialNetwork]:
        docs = await self._collection.find(filters).to_list(length=100)
        return self._mapper.to_domain_list(docs)

    async def exists_by_platform(self, profile_id: str, platform: str) -> bool:
        count = await self._collection.count_documents(
            {"profile_id": profile_id, "platform": platform}
        )
        return count > 0

    async def get_by_platform(
        self, profile_id: str, platform: str
    ) -> SocialNetwork | None:
        doc = await self._collection.find_one(
            {"profile_id": profile_id, "platform": platform}
        )
        if doc is None:
            return None
        return self._mapper.to_domain(doc)

    async def get_by_order_index(
        self, profile_id: str, order_index: int
    ) -> SocialNetwork | None:
        doc = await self._collection.find_one(
            {"profile_id": profile_id, "order_index": order_index}
        )
        if doc is None:
            return None
        return self._mapper.to_domain(doc)

    async def get_all_ordered(
        self, profile_id: str, ascending: bool = True
    ) -> list[SocialNetwork]:
        cursor = self._collection.find({"profile_id": profile_id}).sort(
            "order_index", 1 if ascending else -1
        )
        docs = await cursor.to_list(length=100)
        return self._mapper.to_domain_list(docs)

    async def reorder(
        self, profile_id: str, entity_id: str, new_order_index: int
    ) -> None:
        entity = await self.get_by_id(entity_id)
        if entity is None:
            return

        old_index = entity.order_index

        if old_index == new_order_index:
            return

        if old_index < new_order_index:
            await self._collection.update_many(
                {
                    "profile_id": profile_id,
                    "order_index": {"$gt": old_index, "$lte": new_order_index},
                },
                {"$inc": {"order_index": -1}},
            )
        else:
            await self._collection.update_many(
                {
                    "profile_id": profile_id,
                    "order_index": {"$gte": new_order_index, "$lt": old_index},
                },
                {"$inc": {"order_index": 1}},
            )

        await self._collection.update_one(
            {"_id": entity_id}, {"$set": {"order_index": new_order_index}}
        )