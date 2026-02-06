from datetime import datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities import ContactMessage
from app.infrastructure.mappers import ContactMessageMapper
from app.shared.interfaces.repository import IContactMessageRepository


class ContactMessageRepository(IContactMessageRepository):
    """Concrete implementation of ContactMessage repository using MongoDB."""

    collection_name = "contact_messages"

    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._collection = db[self.collection_name]
        self._mapper = ContactMessageMapper()

    async def add(self, entity: ContactMessage) -> ContactMessage:
        doc = self._mapper.to_persistence(entity)
        await self._collection.insert_one(doc)
        return entity

    async def update(self, entity: ContactMessage) -> ContactMessage:
        doc = self._mapper.to_persistence(entity)
        await self._collection.replace_one({"_id": entity.id}, doc)
        return entity

    async def delete(self, entity_id: str) -> bool:
        result = await self._collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def get_by_id(self, entity_id: str) -> ContactMessage | None:
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
    ) -> list[ContactMessage]:
        cursor = self._collection.find().skip(skip).limit(limit)
        if sort_by:
            cursor = cursor.sort(sort_by, 1 if ascending else -1)
        else:
            cursor = cursor.sort("created_at", -1)  # Default: newest first
        docs = await cursor.to_list(length=limit)
        return self._mapper.to_domain_list(docs)

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        return await self._collection.count_documents(filters or {})

    async def exists(self, entity_id: str) -> bool:
        count = await self._collection.count_documents({"_id": entity_id})
        return count > 0

    async def find_by(self, **filters: Any) -> list[ContactMessage]:
        docs = await self._collection.find(filters).to_list(length=100)
        return self._mapper.to_domain_list(docs)

    async def get_pending_messages(self) -> list[ContactMessage]:
        docs = (
            await self._collection.find({"status": "pending"})
            .sort("created_at", -1)
            .to_list(length=100)
        )
        return self._mapper.to_domain_list(docs)

    async def get_messages_by_status(self, status: str) -> list[ContactMessage]:
        docs = (
            await self._collection.find({"status": status})
            .sort("created_at", -1)
            .to_list(length=100)
        )
        return self._mapper.to_domain_list(docs)

    async def mark_as_read(self, message_id: str) -> bool:
        result = await self._collection.update_one(
            {"_id": message_id, "status": "pending"},
            {"$set": {"status": "read", "read_at": datetime.utcnow()}},
        )
        return result.modified_count > 0

    async def mark_as_replied(self, message_id: str) -> bool:
        now = datetime.utcnow()
        result = await self._collection.update_one(
            {"_id": message_id, "status": {"$in": ["pending", "read"]}},
            {
                "$set": {
                    "status": "replied",
                    "replied_at": now,
                    "read_at": now,  # Ensure read_at is set
                }
            },
        )
        return result.modified_count > 0
