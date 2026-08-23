from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from apps.api.db.models.observation import Observation
from apps.api.db.session import SessionLocal
from apps.api.main import app


client = TestClient(app)


def unique_slug(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex}"


def create_organization(name: str = "Observation Test Organization") -> dict:
    response = client.post(
        "/organizations",
        json={
            "name": name,
            "slug": unique_slug("observation-org"),
        },
    )

    assert response.status_code == 201

    return response.json()


def create_agent(organization_id: str, name: str = "Observation Agent") -> dict:
    response = client.post(
        f"/organizations/{organization_id}/agents",
        json={
            "name": name,
            "agent_type": "shipment",
            "status": "active",
        },
    )

    assert response.status_code == 201

    return response.json()


def observation_payload(
    observation_type: str = "vehicle_delay",
) -> dict:
    return {
        "observation_type": observation_type,
        "subject_type": "vehicle",
        "subject_id": str(uuid4()),
        "observed_value": {
            "delay_minutes": 35,
            "reason": "traffic",
        },
        "source": "carrier_system",
        "confidence": 0.95,
        "event_time": "2026-08-23T10:00:00Z",
    }


def create_observation(
    organization_id: str,
    agent_id: str,
    payload: dict | None = None,
) -> dict:
    response = client.post(
        f"/organizations/{organization_id}/agents/{agent_id}/observations",
        json=payload or observation_payload(),
    )

    assert response.status_code == 201

    return response.json()


def test_create_observation():
    organization = create_organization()
    agent = create_agent(organization["id"])

    response = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}/observations",
        json=observation_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["agent_id"] == agent["id"]
    assert data["observation_type"] == "vehicle_delay"
    assert data["subject_type"] == "vehicle"
    assert data["observed_value"]["delay_minutes"] == 35
    assert data["source"] == "carrier_system"
    assert data["confidence"] == "0.9500"
    assert "id" in data


def test_get_observation():
    organization = create_organization()
    agent = create_agent(organization["id"])
    observation = create_observation(organization["id"], agent["id"])

    response = client.get(
        "/organizations/"
        f"{organization['id']}/agents/{agent['id']}"
        f"/observations/{observation['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == observation["id"]
    assert data["agent_id"] == agent["id"]
    assert data["observation_type"] == "vehicle_delay"


def test_list_observations():
    organization = create_organization()
    agent = create_agent(organization["id"])
    first_observation = create_observation(
        organization["id"],
        agent["id"],
        observation_payload("location_update"),
    )
    second_observation = create_observation(
        organization["id"],
        agent["id"],
        observation_payload("capacity_change"),
    )

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}/observations"
    )

    assert response.status_code == 200

    data = response.json()
    observation_ids = {observation["id"] for observation in data}

    assert first_observation["id"] in observation_ids
    assert second_observation["id"] in observation_ids


def test_observation_belongs_to_correct_agent():
    organization = create_organization()
    agent = create_agent(organization["id"])
    observation = create_observation(organization["id"], agent["id"])

    assert observation["agent_id"] == agent["id"]


def test_observation_belongs_to_correct_organization():
    organization = create_organization()
    agent = create_agent(organization["id"])
    observation = create_observation(organization["id"], agent["id"])

    response = client.get(
        "/organizations/"
        f"{organization['id']}/agents/{agent['id']}"
        f"/observations/{observation['id']}"
    )

    assert response.status_code == 200


def test_nonexistent_agent_returns_not_found():
    organization = create_organization()

    response = client.post(
        f"/organizations/{organization['id']}/agents/{uuid4()}/observations",
        json=observation_payload(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."


def test_nonexistent_observation_returns_not_found():
    organization = create_organization()
    agent = create_agent(organization["id"])

    response = client.get(
        "/organizations/"
        f"{organization['id']}/agents/{agent['id']}"
        f"/observations/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Observation not found."


def test_cross_organization_access_denied():
    first_organization = create_organization("First Observation Organization")
    second_organization = create_organization("Second Observation Organization")
    first_agent = create_agent(first_organization["id"])
    observation = create_observation(first_organization["id"], first_agent["id"])

    response = client.get(
        "/organizations/"
        f"{second_organization['id']}/agents/{first_agent['id']}"
        f"/observations/{observation['id']}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."


def test_invalid_confidence_rejected():
    organization = create_organization()
    agent = create_agent(organization["id"])
    payload = observation_payload()
    payload["confidence"] = 1.5

    response = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}/observations",
        json=payload,
    )

    assert response.status_code == 422


def test_structured_observed_value_works():
    organization = create_organization()
    agent = create_agent(organization["id"])
    payload = observation_payload("warehouse_congestion")
    payload["observed_value"] = {
        "dock": "A3",
        "queue_depth": 7,
        "available_doors": [1, 4, 6],
        "metadata": {
            "reported_by": "warehouse_system",
            "severity": "medium",
        },
    }

    observation = create_observation(
        organization["id"],
        agent["id"],
        payload,
    )

    assert observation["observed_value"]["metadata"]["severity"] == "medium"
    assert observation["observed_value"]["available_doors"] == [1, 4, 6]


def test_multiple_observations_for_one_agent():
    organization = create_organization()
    agent = create_agent(organization["id"])

    for observation_type in [
        "vehicle_delay",
        "location_update",
        "shipment_status",
    ]:
        create_observation(
            organization["id"],
            agent["id"],
            observation_payload(observation_type),
        )

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}/observations"
    )

    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_observation_persists_in_postgresql():
    organization = create_organization()
    agent = create_agent(organization["id"])
    observation = create_observation(organization["id"], agent["id"])

    with SessionLocal() as db:
        persisted_observation = db.scalar(
            select(Observation).where(Observation.id == observation["id"])
        )

    assert persisted_observation is not None
    assert str(persisted_observation.id) == observation["id"]
    assert str(persisted_observation.agent_id) == agent["id"]
    assert persisted_observation.observation_type == "vehicle_delay"
    assert persisted_observation.observed_value["reason"] == "traffic"
