from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.db.models.observation import Observation


class ObservationRepository:
    """Database operations for observations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        agent_id: UUID,
        observation_type: str,
        observed_value: Any,
        event_time: datetime,
        subject_type: str | None = None,
        subject_id: UUID | None = None,
        source: str | None = None,
        confidence: Decimal | None = None,
    ) -> Observation:
        observation = Observation(
            agent_id=agent_id,
            observation_type=observation_type,
            subject_type=subject_type,
            subject_id=subject_id,
            observed_value=observed_value,
            source=source,
            confidence=confidence,
            event_time=event_time,
        )

        self.db.add(observation)
        self.db.flush()

        return observation

    def get_by_id(
        self,
        observation_id: UUID,
    ) -> Observation | None:
        statement = select(Observation).where(
            Observation.id == observation_id
        )

        return self.db.scalar(statement)

    def list_by_agent(
        self,
        agent_id: UUID,
    ) -> list[Observation]:
        statement = (
            select(Observation)
            .where(Observation.agent_id == agent_id)
            .order_by(Observation.event_time, Observation.created_at, Observation.id)
        )

        return list(self.db.scalars(statement))
