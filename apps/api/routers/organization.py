from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.db.session import get_db
from apps.api.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)
from apps.api.services.organization import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    service = OrganizationService(db)

    try:
        organization = service.create_organization(
            name=payload.name,
            slug=payload.slug,
        )

        return organization

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    service = OrganizationService(db)

    organization = service.get_organization(
        organization_id
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    return organization
