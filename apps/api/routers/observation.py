from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.db.session import get_db
from apps.api.schemas.observation import (
    ObservationCreate,
    ObservationResponse,
)
from apps.api.services.observation import ObservationService


router = APIRouter(
    prefix="/organizations/{organization_id}/agents/{agent_id}/observations",
    tags=["Observations"],
)


@router.post(
    "",
    response_model=ObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_observation(
    organization_id: UUID,
    agent_id: UUID,
    payload: ObservationCreate,
    db: Session = Depends(get_db),
) -> ObservationResponse:
    service = ObservationService(db)

    try:
        observation = service.create_observation(
            organization_id=organization_id,
            agent_id=agent_id,
            observation_type=payload.observation_type,
            observed_value=payload.observed_value,
            event_time=payload.event_time,
            subject_type=payload.subject_type,
            subject_id=payload.subject_id,
            source=payload.source,
            confidence=payload.confidence,
        )

        return observation

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
    response_model=list[ObservationResponse],
)
def list_observations(
    organization_id: UUID,
    agent_id: UUID,
    db: Session = Depends(get_db),
) -> list[ObservationResponse]:
    service = ObservationService(db)

    try:
        return service.list_observations(
            organization_id=organization_id,
            agent_id=agent_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{observation_id}",
    response_model=ObservationResponse,
)
def get_observation(
    organization_id: UUID,
    agent_id: UUID,
    observation_id: UUID,
    db: Session = Depends(get_db),
) -> ObservationResponse:
    service = ObservationService(db)

    try:
        observation = service.get_observation(
            organization_id=organization_id,
            agent_id=agent_id,
            observation_id=observation_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found.",
        )

    return observation
