from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from apps.api.db.models.agent import Agent
from apps.api.db.session import SessionLocal
from apps.api.main import app


client = TestClient(app)


def unique_slug(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex}"


def create_organization(name: str = "Agent Test Organization") -> dict:
    response = client.post(
        "/organizations",
        json={
            "name": name,
            "slug": unique_slug("agent-org"),
        },
    )

    assert response.status_code == 201

    return response.json()


def create_agent(
    organization_id: str,
    name: str = "Shipment Coordinator",
    agent_type: str = "shipment",
    status: str = "active",
) -> dict:
    response = client.post(
        f"/organizations/{organization_id}/agents",
        json={
            "name": name,
            "agent_type": agent_type,
            "status": status,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_agent():
    organization = create_organization()

    response = client.post(
        f"/organizations/{organization['id']}/agents",
        json={
            "name": "Carrier Reliability Agent",
            "agent_type": "carrier",
            "status": "active",
            "entity_type": "carrier",
            "entity_id": str(uuid4()),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["organization_id"] == organization["id"]
    assert data["name"] == "Carrier Reliability Agent"
    assert data["agent_type"] == "carrier"
    assert data["status"] == "active"
    assert data["entity_type"] == "carrier"
    assert "id" in data


def test_get_agent():
    organization = create_organization()
    agent = create_agent(organization["id"])

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == agent["id"]
    assert data["organization_id"] == organization["id"]
    assert data["name"] == "Shipment Coordinator"


def test_list_agents():
    organization = create_organization()

    first_agent = create_agent(
        organization["id"],
        name="First Agent",
        agent_type="shipment",
    )
    second_agent = create_agent(
        organization["id"],
        name="Second Agent",
        agent_type="warehouse",
    )

    response = client.get(f"/organizations/{organization['id']}/agents")

    assert response.status_code == 200

    data = response.json()
    agent_ids = {agent["id"] for agent in data}

    assert first_agent["id"] in agent_ids
    assert second_agent["id"] in agent_ids


def test_agent_belongs_to_correct_organization():
    organization = create_organization()
    agent = create_agent(organization["id"])

    assert agent["organization_id"] == organization["id"]


def test_nonexistent_agent_returns_not_found():
    organization = create_organization()

    response = client.get(
        f"/organizations/{organization['id']}/agents/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."


def test_agent_cannot_be_accessed_through_another_organization():
    first_organization = create_organization("First Agent Organization")
    second_organization = create_organization("Second Agent Organization")
    agent = create_agent(first_organization["id"])

    response = client.get(
        "/organizations/"
        f"{second_organization['id']}/agents/{agent['id']}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."


def test_database_persistence():
    organization = create_organization()
    agent = create_agent(
        organization["id"],
        name="Persistent Agent",
        agent_type="hub",
    )

    with SessionLocal() as db:
        persisted_agent = db.scalar(
            select(Agent).where(Agent.id == agent["id"])
        )

    assert persisted_agent is not None
    assert str(persisted_agent.id) == agent["id"]
    assert str(persisted_agent.organization_id) == organization["id"]
    assert persisted_agent.name == "Persistent Agent"
    assert persisted_agent.agent_type == "hub"
