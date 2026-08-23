from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ObservationCreate(BaseModel):
    observation_type: str = Field(
        min_length=1,
        max_length=100,
    )

    subject_type: str | None = Field(
        default=None,
        max_length=100,
    )

    subject_id: UUID | None = None

    observed_value: Any

    source: str | None = Field(
        default=None,
        max_length=100,
    )

    confidence: Decimal | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    event_time: datetime


class ObservationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    agent_id: UUID
    observation_type: str
    subject_type: str | None
    subject_id: UUID | None
    observed_value: Any
    source: str | None
    confidence: Decimal | None
    event_time: datetime
    observed_at: datetime
    created_at: datetime
    updated_at: datetime
