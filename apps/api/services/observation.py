from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from apps.api.db.models.observation import Observation
from apps.api.repositories.agent import AgentRepository
from apps.api.repositories.observation import ObservationRepository
from apps.api.repositories.organization import OrganizationRepository


class ObservationService:
    """Business logic for observations."""

    def __init__(self, db: Session) -> None:
        self.repository = ObservationRepository(db)
        self.agent_repository = AgentRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.db = db

    def create_observation(
        self,
        organization_id: UUID,
        agent_id: UUID,
        observation_type: str,
        observed_value: Any,
        event_time: datetime,
        subject_type: str | None = None,
        subject_id: UUID | None = None,
        source: str | None = None,
        confidence: Decimal | None = None,
    ) -> Observation:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        normalized_observation_type = observation_type.strip().lower()
        normalized_subject_type = (
            subject_type.strip().lower()
            if subject_type is not None
            else None
        )
        normalized_source = (
            source.strip().lower()
            if source is not None
            else None
        )

        if not normalized_observation_type:
            raise ValueError("Observation type cannot be empty.")

        if normalized_subject_type == "":
            normalized_subject_type = None

        if normalized_source == "":
            normalized_source = None

        observation = self.repository.create(
            agent_id=agent_id,
            observation_type=normalized_observation_type,
            observed_value=observed_value,
            event_time=event_time,
            subject_type=normalized_subject_type,
            subject_id=subject_id,
            source=normalized_source,
            confidence=confidence,
        )

        self.db.commit()
        self.db.refresh(observation)

        return observation

    def get_observation(
        self,
        organization_id: UUID,
        agent_id: UUID,
        observation_id: UUID,
    ) -> Observation | None:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        observation = self.repository.get_by_id(observation_id)

        if observation is None or observation.agent_id != agent_id:
            return None

        return observation

    def list_observations(
        self,
        organization_id: UUID,
        agent_id: UUID,
    ) -> list[Observation]:
        self._require_agent_for_organization(
            organization_id=organization_id,
            agent_id=agent_id,
        )

        return self.repository.list_by_agent(agent_id)

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
