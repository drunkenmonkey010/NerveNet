from uuid import UUID

from sqlalchemy.orm import Session

from apps.api.db.models.agent import Agent
from apps.api.repositories.agent import AgentRepository
from apps.api.repositories.organization import OrganizationRepository


class AgentService:
    """Business logic for agents."""

    def __init__(self, db: Session) -> None:
        self.repository = AgentRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.db = db

    def create_agent(
        self,
        organization_id: UUID,
        name: str,
        agent_type: str,
        status: str,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
    ) -> Agent:
        self._require_organization(organization_id)

        normalized_name = name.strip()
        normalized_agent_type = agent_type.strip().lower()
        normalized_status = status.strip().lower()
        normalized_entity_type = (
            entity_type.strip().lower()
            if entity_type is not None
            else None
        )

        if not normalized_name:
            raise ValueError("Agent name cannot be empty.")

        if not normalized_agent_type:
            raise ValueError("Agent type cannot be empty.")

        if not normalized_status:
            raise ValueError("Agent status cannot be empty.")

        if normalized_entity_type == "":
            normalized_entity_type = None

        agent = self.repository.create(
            organization_id=organization_id,
            name=normalized_name,
            agent_type=normalized_agent_type,
            status=normalized_status,
            entity_type=normalized_entity_type,
            entity_id=entity_id,
        )

        self.db.commit()
        self.db.refresh(agent)

        return agent

    def get_agent(
        self,
        organization_id: UUID,
        agent_id: UUID,
    ) -> Agent | None:
        self._require_organization(organization_id)

        agent = self.repository.get_by_id(agent_id)

        if agent is None or agent.organization_id != organization_id:
            return None

        return agent

    def list_agents(
        self,
        organization_id: UUID,
    ) -> list[Agent]:
        self._require_organization(organization_id)

        return self.repository.list_by_organization(organization_id)

    def _require_organization(
        self,
        organization_id: UUID,
    ) -> None:
        organization = self.organization_repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise LookupError("Organization not found.")
