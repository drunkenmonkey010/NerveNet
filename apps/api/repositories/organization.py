from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.db.models.organization import Organization


class OrganizationRepository:
    """Database operations for organizations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        name: str,
        slug: str,
    ) -> Organization:
        organization = Organization(
            name=name,
            slug=slug,
        )

        self.db.add(organization)
        self.db.flush()

        return organization

    def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        statement = select(Organization).where(
            Organization.id == organization_id
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        statement = select(Organization).where(
            Organization.slug == slug
        )

        return self.db.scalar(statement)