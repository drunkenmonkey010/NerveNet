from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from apps.api.db.models.organization import Organization
from apps.api.db.session import SessionLocal
from apps.api.main import app


client = TestClient(app)


def unique_slug(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex}"


def test_create_organization():
    slug = unique_slug("create")

    response = client.post(
        "/organizations",
        json={
            "name": "Create Test Organization",
            "slug": slug,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Create Test Organization"
    assert data["slug"] == slug
    assert "id" in data


def test_get_organization():
    slug = unique_slug("get")

    create_response = client.post(
        "/organizations",
        json={
            "name": "Get Test Organization",
            "slug": slug,
        },
    )

    organization_id = create_response.json()["id"]

    response = client.get(f"/organizations/{organization_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["name"] == "Get Test Organization"
    assert data["slug"] == slug


def test_get_nonexistent_organization():
    response = client.get(f"/organizations/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found."


def test_duplicate_slug():
    slug = unique_slug("duplicate")

    first_response = client.post(
        "/organizations",
        json={
            "name": "First Duplicate Test Organization",
            "slug": slug,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/organizations",
        json={
            "name": "Second Duplicate Test Organization",
            "slug": slug,
        },
    )

    assert second_response.status_code == 400
    assert "already exists" in second_response.json()["detail"]


def test_invalid_organization_name():
    response = client.post(
        "/organizations",
        json={
            "name": "   ",
            "slug": unique_slug("invalid"),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Organization name cannot be empty."


def test_database_persistence():
    slug = unique_slug("persistence")

    response = client.post(
        "/organizations",
        json={
            "name": "Persistence Test Organization",
            "slug": slug,
        },
    )

    assert response.status_code == 201

    organization_id = response.json()["id"]

    with SessionLocal() as db:
        organization = db.scalar(
            select(Organization).where(Organization.slug == slug)
        )

    assert organization is not None
    assert str(organization.id) == organization_id
    assert organization.name == "Persistence Test Organization"
