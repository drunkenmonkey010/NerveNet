from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from apps.api.db.models.memory_event import MemoryEvent
from apps.api.db.session import SessionLocal
from apps.api.main import app


client = TestClient(app)


def unique_slug(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex}"


def create_organization(name: str = "Memory Test Organization") -> dict:
    response = client.post(
        "/organizations",
        json={
            "name": name,
            "slug": unique_slug("memory-org"),
        },
    )

    assert response.status_code == 201

    return response.json()


def create_agent(organization_id: str, name: str = "Memory Agent") -> dict:
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


def observation_payload() -> dict:
    return {
        "observation_type": "vehicle_delay",
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


def create_observation(organization_id: str, agent_id: str) -> dict:
    response = client.post(
        f"/organizations/{organization_id}/agents/{agent_id}/observations",
        json=observation_payload(),
    )

    assert response.status_code == 201

    return response.json()


def memory_payload(memory_type: str = "episodic") -> dict:
    return {
        "memory_type": memory_type,
        "content": {
            "event": "vehicle_delay",
            "delay_minutes": 35,
        },
        "importance": 0.8,
        "event_time": "2026-08-23T10:00:00Z",
    }


def create_memory(
    organization_id: str,
    agent_id: str,
    payload: dict | None = None,
) -> dict:
    response = client.post(
        f"/organizations/{organization_id}/agents/{agent_id}/memories",
        json=payload or memory_payload(),
    )

    assert response.status_code == 201

    return response.json()


def test_create_memory_directly():
    organization = create_organization()
    agent = create_agent(organization["id"])

    response = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}/memories",
        json=memory_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["agent_id"] == agent["id"]
    assert data["memory_type"] == "episodic"
    assert data["content"]["delay_minutes"] == 35
    assert data["importance"] == "0.8000"
    assert "id" in data


def test_get_memory():
    organization = create_organization()
    agent = create_agent(organization["id"])
    memory = create_memory(organization["id"], agent["id"])

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
        f"/memories/{memory['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == memory["id"]
    assert data["agent_id"] == agent["id"]
    assert data["memory_type"] == "episodic"


def test_list_memories():
    organization = create_organization()
    agent = create_agent(organization["id"])
    first_memory = create_memory(
        organization["id"],
        agent["id"],
        memory_payload("episodic"),
    )
    second_memory = create_memory(
        organization["id"],
        agent["id"],
        memory_payload("interaction"),
    )

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}/memories"
    )

    assert response.status_code == 200

    data = response.json()
    memory_ids = {memory["id"] for memory in data}

    assert first_memory["id"] in memory_ids
    assert second_memory["id"] in memory_ids


def test_memory_belongs_to_correct_agent():
    organization = create_organization()
    agent = create_agent(organization["id"])
    memory = create_memory(organization["id"], agent["id"])

    assert memory["agent_id"] == agent["id"]


def test_memory_belongs_to_correct_organization():
    organization = create_organization()
    agent = create_agent(organization["id"])
    memory = create_memory(organization["id"], agent["id"])

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
        f"/memories/{memory['id']}"
    )

    assert response.status_code == 200


def test_create_memory_from_observation():
    organization = create_organization()
    agent = create_agent(organization["id"])
    observation = create_observation(organization["id"], agent["id"])

    response = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
        f"/observations/{observation['id']}/memory",
        json={
            "memory_type": "episodic",
            "importance": 0.75,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["agent_id"] == agent["id"]
    assert data["memory_type"] == "episodic"
    assert data["source_type"] == "observation"
    assert data["source_id"] == observation["id"]
    assert data["content"]["observation_type"] == "vehicle_delay"
    assert data["content"]["observed_value"]["delay_minutes"] == 35


def test_observation_to_memory_provenance_is_preserved():
    organization = create_organization()
    agent = create_agent(organization["id"])
    observation = create_observation(organization["id"], agent["id"])

    memory = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
        f"/observations/{observation['id']}/memory",
        json={
            "memory_type": "episodic",
        },
    ).json()

    assert memory["source_type"] == "observation"
    assert memory["source_id"] == observation["id"]
    assert memory["content"]["source"] == "carrier_system"
    assert memory["content"]["confidence"] == "0.9500"


def test_nonexistent_agent_returns_not_found():
    organization = create_organization()

    response = client.post(
        f"/organizations/{organization['id']}/agents/{uuid4()}/memories",
        json=memory_payload(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."


def test_nonexistent_memory_returns_not_found():
    organization = create_organization()
    agent = create_agent(organization["id"])

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
        f"/memories/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Memory not found."


def test_nonexistent_observation_returns_not_found():
    organization = create_organization()
    agent = create_agent(organization["id"])

    response = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}"
        f"/observations/{uuid4()}/memory",
        json={
            "memory_type": "episodic",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Observation not found."


def test_cross_organization_access_denied():
    first_organization = create_organization("First Memory Organization")
    second_organization = create_organization("Second Memory Organization")
    first_agent = create_agent(first_organization["id"])
    memory = create_memory(first_organization["id"], first_agent["id"])

    response = client.get(
        f"/organizations/{second_organization['id']}/agents/{first_agent['id']}"
        f"/memories/{memory['id']}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."


def test_invalid_importance_rejected():
    organization = create_organization()
    agent = create_agent(organization["id"])
    payload = memory_payload()
    payload["importance"] = 1.5

    response = client.post(
        f"/organizations/{organization['id']}/agents/{agent['id']}/memories",
        json=payload,
    )

    assert response.status_code == 422


def test_structured_json_content_works():
    organization = create_organization()
    agent = create_agent(organization["id"])
    payload = memory_payload("semantic")
    payload["content"] = {
        "lane": "BLR-HYD",
        "patterns": [
            {
                "event": "delay",
                "count": 3,
            }
        ],
        "metadata": {
            "summary_method": "manual",
            "reviewed": True,
        },
    }

    memory = create_memory(organization["id"], agent["id"], payload)

    assert memory["content"]["metadata"]["reviewed"] is True
    assert memory["content"]["patterns"][0]["count"] == 3


def test_multiple_memories_for_one_agent():
    organization = create_organization()
    agent = create_agent(organization["id"])

    for memory_type in ["episodic", "interaction", "outcome"]:
        create_memory(
            organization["id"],
            agent["id"],
            memory_payload(memory_type),
        )

    response = client.get(
        f"/organizations/{organization['id']}/agents/{agent['id']}/memories"
    )

    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_memory_persists_in_postgresql():
    organization = create_organization()
    agent = create_agent(organization["id"])
    memory = create_memory(organization["id"], agent["id"])

    with SessionLocal() as db:
        persisted_memory = db.scalar(
            select(MemoryEvent).where(MemoryEvent.id == memory["id"])
        )

    assert persisted_memory is not None
    assert str(persisted_memory.id) == memory["id"]
    assert str(persisted_memory.agent_id) == agent["id"]
    assert persisted_memory.memory_type == "episodic"
    assert persisted_memory.content["event"] == "vehicle_delay"
