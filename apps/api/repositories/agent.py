from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from apps.api.db.models.agent import Agent


class AgentRepository:
    """Database operations for agents."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        organization_id: UUID,
        name: str,
        agent_type: str,
        status: str,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
    ) -> Agent:
        agent = Agent(
            organization_id=organization_id,
            name=name,
            agent_type=agent_type,
            status=status,
            entity_type=entity_type,
            entity_id=entity_id,
        )

        self.db.add(agent)
        self.db.flush()

        return agent

    def get_by_id(
        self,
        agent_id: UUID,
    ) -> Agent | None:
        statement = select(Agent).where(Agent.id == agent_id)

        return self.db.scalar(statement)

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Agent]:
        statement = (
            select(Agent)
            .where(Agent.organization_id == organization_id)
            .order_by(Agent.created_at, Agent.id)
        )

        return list(self.db.scalars(statement))

    def exists_for_organization(
        self,
        organization_id: UUID,
        agent_id: UUID,
    ) -> bool:
        statement = select(
            exists().where(
                Agent.id == agent_id,
                Agent.organization_id == organization_id,
            )
        )

        return bool(self.db.scalar(statement))
