from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from apps.api.db.session import get_db
from apps.api.schemas.memory_event import (
    MemoryEventCreate,
    MemoryEventResponse,
    MemoryFromObservationCreate,
)
from apps.api.services.memory_event import MemoryEventService


router = APIRouter(
    prefix="/organizations/{organization_id}/agents/{agent_id}",
    tags=["Memory Events"],
)


@router.post(
    "/memories",
    response_model=MemoryEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_memory(
    organization_id: UUID,
    agent_id: UUID,
    payload: MemoryEventCreate,
    db: Session = Depends(get_db),
) -> MemoryEventResponse:
    service = MemoryEventService(db)

    try:
        memory = service.create_memory(
            organization_id=organization_id,
            agent_id=agent_id,
            memory_type=payload.memory_type,
            content=payload.content,
            event_time=payload.event_time,
            source_type=payload.source_type,
            source_id=payload.source_id,
            importance=payload.importance,
        )

        return memory

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
    "/memories",
    response_model=list[MemoryEventResponse],
)
def list_memories(
    organization_id: UUID,
    agent_id: UUID,
    memory_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[MemoryEventResponse]:
    service = MemoryEventService(db)

    try:
        return service.list_memories(
            organization_id=organization_id,
            agent_id=agent_id,
            memory_type=memory_type,
        )

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
    "/memories/{memory_id}",
    response_model=MemoryEventResponse,
)
def get_memory(
    organization_id: UUID,
    agent_id: UUID,
    memory_id: UUID,
    db: Session = Depends(get_db),
) -> MemoryEventResponse:
    service = MemoryEventService(db)

    try:
        memory = service.get_memory(
            organization_id=organization_id,
            agent_id=agent_id,
            memory_id=memory_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found.",
        )

    return memory


@router.post(
    "/observations/{observation_id}/memory",
    response_model=MemoryEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_memory_from_observation(
    organization_id: UUID,
    agent_id: UUID,
    observation_id: UUID,
    payload: MemoryFromObservationCreate,
    db: Session = Depends(get_db),
) -> MemoryEventResponse:
    service = MemoryEventService(db)

    try:
        memory = service.create_memory_from_observation(
            organization_id=organization_id,
            agent_id=agent_id,
            observation_id=observation_id,
            memory_type=payload.memory_type,
            importance=payload.importance,
            event_time=payload.event_time,
        )

        return memory

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
