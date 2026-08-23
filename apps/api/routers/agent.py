from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.db.session import get_db
from apps.api.schemas.agent import AgentCreate, AgentResponse
from apps.api.services.agent import AgentService


router = APIRouter(
    prefix="/organizations/{organization_id}/agents",
    tags=["Agents"],
)


@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_agent(
    organization_id: UUID,
    payload: AgentCreate,
    db: Session = Depends(get_db),
) -> AgentResponse:
    service = AgentService(db)

    try:
        agent = service.create_agent(
            organization_id=organization_id,
            name=payload.name,
            agent_type=payload.agent_type,
            status=payload.status,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
        )

        return agent

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[AgentResponse],
)
def list_agents(
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> list[AgentResponse]:
    service = AgentService(db)

    try:
        return service.list_agents(organization_id)

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
def get_agent(
    organization_id: UUID,
    agent_id: UUID,
    db: Session = Depends(get_db),
) -> AgentResponse:
    service = AgentService(db)

    try:
        agent = service.get_agent(
            organization_id=organization_id,
            agent_id=agent_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    return agent
