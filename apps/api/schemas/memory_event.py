from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MemoryEventCreate(BaseModel):
    memory_type: str = Field(
        min_length=1,
        max_length=100,
    )

    source_type: str | None = Field(
        default=None,
        max_length=100,
    )

    source_id: UUID | None = None

    content: Any

    importance: Decimal | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    event_time: datetime


class MemoryFromObservationCreate(BaseModel):
    memory_type: str = Field(
        min_length=1,
        max_length=100,
    )

    importance: Decimal | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    event_time: datetime | None = None


class MemoryEventResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    agent_id: UUID
    memory_type: str
    source_type: str | None
    source_id: UUID | None
    content: Any
    importance: Decimal | None
    event_time: datetime
    created_at: datetime
    updated_at: datetime
