from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
    )

    agent_type: str = Field(
        min_length=1,
        max_length=100,
    )

    status: str = Field(
        min_length=1,
        max_length=100,
    )

    entity_type: str | None = Field(
        default=None,
        max_length=100,
    )

    entity_id: UUID | None = None


class AgentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    organization_id: UUID
    name: str
    agent_type: str
    status: str
    entity_type: str | None
    entity_id: UUID | None
    created_at: datetime
    updated_at: datetime
