from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from apps.api.db.models.memory_event import MemoryEvent
from apps.api.db.models.observation import Observation
from apps.api.repositories.agent import AgentRepository
from apps.api.repositories.memory_event import MemoryEventRepository
from apps.api.repositories.observation import ObservationRepository
from apps.api.repositories.organization import OrganizationRepository


class MemoryEventService:
    """Business logic for memory events."""

    def __init__(self, db: Session) -> None:
        self.repository = MemoryEventRepository(db)
        self.agent_repository = AgentRepository(db)
        self.observation_repository = ObservationRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.db = db

    def create_memory(
        self,
        organization_id: UUID,
        agent_id: UUID,
        memory_type: str,
        content: Any,
        event_time: datetime,
        source_type: str | None = None,
        source_id: UUID | None = None,
        importance: Decimal | None = None,
    ) -> MemoryEvent:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        normalized_memory_type = memory_type.strip().lower()
        normalized_source_type = (
            source_type.strip().lower()
            if source_type is not None
            else None
        )

        if not normalized_memory_type:
            raise ValueError("Memory type cannot be empty.")

        if normalized_source_type == "":
            normalized_source_type = None

        memory = self.repository.create(
            agent_id=agent_id,
            memory_type=normalized_memory_type,
            content=content,
            event_time=event_time,
            source_type=normalized_source_type,
            source_id=source_id,
            importance=importance,
        )

        self.db.commit()
        self.db.refresh(memory)

        return memory

    def create_memory_from_observation(
        self,
        organization_id: UUID,
        agent_id: UUID,
        observation_id: UUID,
        memory_type: str,
        importance: Decimal | None = None,
        event_time: datetime | None = None,
    ) -> MemoryEvent:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        observation = self._require_observation_for_agent(
            agent_id=agent_id,
            observation_id=observation_id,
        )

        content = self._memory_content_from_observation(observation)

        return self.create_memory(
            organization_id=organization_id,
            agent_id=agent_id,
            memory_type=memory_type,
            content=content,
            event_time=event_time or observation.event_time,
            source_type="observation",
            source_id=observation.id,
            importance=importance,
        )

    def get_memory(
        self,
        organization_id: UUID,
        agent_id: UUID,
        memory_id: UUID,
    ) -> MemoryEvent | None:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        memory = self.repository.get_by_id(memory_id)

        if memory is None or memory.agent_id != agent_id:
            return None

        return memory

    def list_memories(
        self,
        organization_id: UUID,
        agent_id: UUID,
        memory_type: str | None = None,
    ) -> list[MemoryEvent]:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        if memory_type is None:
            return self.repository.list_by_agent(agent_id)

        normalized_memory_type = memory_type.strip().lower()

        if not normalized_memory_type:
            raise ValueError("Memory type cannot be empty.")

        return self.repository.list_by_agent_and_memory_type(
            agent_id=agent_id,
            memory_type=normalized_memory_type,
        )

    def _require_agent_for_organization(
        self,
        organization_id: UUID,
        agent_id: UUID,
    ) -> None:
        organization = self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise LookupError("Organization not found.")

        agent = self.agent_repository.get_by_id(agent_id)

        if agent is None:
            raise LookupError("Agent not found.")

        if agent.organization_id != organization_id:
            raise LookupError("Agent not found.")

    def _require_observation_for_agent(
        self,
        agent_id: UUID,
        observation_id: UUID,
    ) -> Observation:
        observation = self.observation_repository.get_by_id(observation_id)

        if observation is None:
            raise LookupError("Observation not found.")

        if observation.agent_id != agent_id:
            raise LookupError("Observation not found.")

        return observation

    @staticmethod
    def _memory_content_from_observation(
        observation: Observation,
    ) -> dict[str, Any]:
        return {
            "observation_type": observation.observation_type,
            "observed_value": observation.observed_value,
            "subject_type": observation.subject_type,
            "subject_id": str(observation.subject_id)
            if observation.subject_id is not None
            else None,
            "source": observation.source,
            "confidence": str(observation.confidence)
            if observation.confidence is not None
            else None,
            "event_time": observation.event_time.isoformat(),
        }
