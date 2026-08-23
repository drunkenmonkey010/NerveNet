from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.db.models.memory_event import MemoryEvent


class MemoryEventRepository:
    """Database operations for memory events."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        agent_id: UUID,
        memory_type: str,
        content: Any,
        event_time: datetime,
        source_type: str | None = None,
        source_id: UUID | None = None,
        importance: Decimal | None = None,
    ) -> MemoryEvent:
        memory = MemoryEvent(
            agent_id=agent_id,
            memory_type=memory_type,
            source_type=source_type,
            source_id=source_id,
            content=content,
            importance=importance,
            event_time=event_time,
        )

        self.db.add(memory)
        self.db.flush()

        return memory

    def get_by_id(
        self,
        memory_id: UUID,
    ) -> MemoryEvent | None:
        statement = select(MemoryEvent).where(MemoryEvent.id == memory_id)

        return self.db.scalar(statement)

    def list_by_agent(
        self,
        agent_id: UUID,
    ) -> list[MemoryEvent]:
        statement = (
            select(MemoryEvent)
            .where(MemoryEvent.agent_id == agent_id)
            .order_by(MemoryEvent.event_time, MemoryEvent.created_at, MemoryEvent.id)
        )

        return list(self.db.scalars(statement))

    def list_by_agent_and_memory_type(
        self,
        agent_id: UUID,
        memory_type: str,
    ) -> list[MemoryEvent]:
        statement = (
            select(MemoryEvent)
            .where(
                MemoryEvent.agent_id == agent_id,
                MemoryEvent.memory_type == memory_type,
            )
            .order_by(MemoryEvent.event_time, MemoryEvent.created_at, MemoryEvent.id)
        )

        return list(self.db.scalars(statement))

    def list_by_source(
        self,
        source_type: str,
        source_id: UUID,
    ) -> list[MemoryEvent]:
        statement = (
            select(MemoryEvent)
            .where(
                MemoryEvent.source_type == source_type,
                MemoryEvent.source_id == source_id,
            )
            .order_by(MemoryEvent.created_at, MemoryEvent.id)
        )

        return list(self.db.scalars(statement))
