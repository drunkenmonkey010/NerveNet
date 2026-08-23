import re
from uuid import UUID

from sqlalchemy.orm import Session

from apps.api.db.models.organization import Organization
from apps.api.repositories.organization import OrganizationRepository


class OrganizationService:
    """Business logic for organizations."""

    def __init__(self, db: Session) -> None:
        self.repository = OrganizationRepository(db)
        self.db = db

    def create_organization(
        self,
        name: str,
        slug: str | None = None,
    ) -> Organization:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Organization name cannot be empty.")

        normalized_slug = (
            slug.strip().lower()
            if slug
            else self._generate_slug(normalized_name)
        )

        if not normalized_slug:
            raise ValueError("Organization slug cannot be empty.")

        existing = self.repository.get_by_slug(normalized_slug)

        if existing:
            raise ValueError(
                f"Organization slug '{normalized_slug}' already exists."
            )

        organization = self.repository.create(
            name=normalized_name,
            slug=normalized_slug,
        )

        self.db.commit()
        self.db.refresh(organization)

        return organization

    def get_organization(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        return self.repository.get_by_id(organization_id)

    @staticmethod
    def _generate_slug(name: str) -> str:
        slug = name.lower().strip()

        slug = re.sub(
            r"[^a-z0-9]+",
            "-",
            slug,
        )

        slug = slug.strip("-")

        return slug
