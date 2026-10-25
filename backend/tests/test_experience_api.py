from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Experience, Skill


@pytest.fixture
def experience_payload() -> dict:
    """Return a valid experience creation payload."""

    return {
        "company": "Example Company",
        "designation": "Python Developer",
        "employment_type": "Full-time",
        "location": "Hyderabad",
        "location_type": "Hybrid",
        "start_date": "2024-01-01",
        "end_date": None,
        "is_current": True,
        "description": "Backend development.",
        "display_order": 1,
    }


@pytest.fixture
def experience(
    db_session: Session,
) -> Experience:
    """Create an experience directly in the test database."""

    item = Experience(
        company="Example Company",
        designation="Python Developer",
        employment_type="Full-time",
        location="Hyderabad",
        location_type="Hybrid",
        start_date=date(2024, 1, 1),
        end_date=None,
        is_current=True,
        description="Backend development.",
        display_order=1,
    )

    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    return item


@pytest.fixture
def second_experience(
    db_session: Session,
) -> Experience:
    """Create a second, distinct experience."""

    item = Experience(
        company="Another Company",
        designation="Software Engineer",
        employment_type="Contract",
        location="Bengaluru",
        location_type="Remote",
        start_date=date(2022, 1, 1),
        end_date=date(2023, 12, 31),
        is_current=False,
        description="Software development.",
        display_order=2,
    )

    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    return item


@pytest.fixture
def skill(
    db_session: Session,
) -> Skill:
    """Create a skill directly in the test database."""

    item = Skill(
        name="Python",
        category="Backend",
        proficiency=90,
        display_order=1,
    )

    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    return item


@pytest.fixture
def second_skill(
    db_session: Session,
) -> Skill:
    """Create a second skill directly in the test database."""

    item = Skill(
        name="FastAPI",
        category="Backend",
        proficiency=85,
        display_order=2,
    )

    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    return item


# =========================================================
# List and retrieval
# =========================================================


def test_list_experiences_empty(client: TestClient):
    response = client.get("/api/v1/experiences")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Experiences retrieved successfully."
    assert body["data"] == []


def test_list_experiences(
    client: TestClient,
    experience: Experience,
):
    response = client.get("/api/v1/experiences")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == experience.id
    assert body["data"][0]["company"] == "Example Company"


def test_get_experience_by_id(
    client: TestClient,
    experience: Experience,
):
    response = client.get(
        f"/api/v1/experiences/{experience.id}"
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Experience retrieved successfully."
    assert body["data"]["id"] == experience.id
    assert body["data"]["designation"] == "Python Developer"


def test_get_missing_experience(client: TestClient):
    response = client.get("/api/v1/experiences/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


# =========================================================
# Filters and current employment
# =========================================================


def test_filter_experiences_by_company(
    client: TestClient,
    experience: Experience,
    second_experience: Experience,
):
    response = client.get(
        "/api/v1/experiences",
        params={"company": "Example"},
    )

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == experience.id


def test_filter_experiences_by_employment_type(
    client: TestClient,
    experience: Experience,
    second_experience: Experience,
):
    response = client.get(
        "/api/v1/experiences",
        params={"employment_type": "Contract"},
    )

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == second_experience.id


def test_filter_experiences_by_location_type(
    client: TestClient,
    experience: Experience,
    second_experience: Experience,
):
    response = client.get(
        "/api/v1/experiences",
        params={"location_type": "Remote"},
    )

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == second_experience.id

def test_filter_experiences_with_multiple_filters(
    client: TestClient,
    experience: Experience,
    second_experience: Experience,
):
    response = client.get(
        "/api/v1/experiences",
        params={
            "company": "Example",
            "employment_type": "Full-time",
            "location_type": "Hybrid",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == experience.id

def test_filter_experiences_by_company_case_insensitive(
    client: TestClient,
    experience: Experience,
):
    response = client.get(
        "/api/v1/experiences",
        params={"company": "eXaMpLe"},
    )

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == experience.id


def test_get_current_experiences(
    client: TestClient,
    experience: Experience,
    second_experience: Experience,
):
    response = client.get("/api/v1/experiences/current")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Current experiences retrieved successfully."
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == experience.id
    assert body["data"][0]["is_current"] is True


# =========================================================
# Create
# =========================================================


def test_create_experience(
    client: TestClient,
    experience_payload: dict,
):
    response = client.post(
        "/api/v1/experiences",
        json=experience_payload,
    )

    assert response.status_code == 201

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Experience created successfully."
    assert body["data"]["company"] == "Example Company"
    assert body["data"]["designation"] == "Python Developer"
    assert body["data"]["is_current"] is True
    assert body["data"]["id"] is not None


def test_create_duplicate_experience(
    client: TestClient,
    experience_payload: dict,
    experience: Experience,
):
    response = client.post(
        "/api/v1/experiences",
        json=experience_payload,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "An experience with the same company, "
        "designation, and start date already exists."
    )


def test_create_experience_with_invalid_date_range(
    client: TestClient,
    experience_payload: dict,
):
    experience_payload["start_date"] = "2025-01-01"
    experience_payload["end_date"] = "2024-01-01"
    experience_payload["is_current"] = False

    response = client.post(
        "/api/v1/experiences",
        json=experience_payload,
    )

    assert response.status_code == 422


def test_create_current_experience_with_end_date(
    client: TestClient,
    experience_payload: dict,
):
    experience_payload["end_date"] = "2025-01-01"

    response = client.post(
        "/api/v1/experiences",
        json=experience_payload,
    )

    assert response.status_code == 422


def test_create_experience_with_invalid_data(
    client: TestClient,
    experience_payload: dict,
):
    experience_payload["company"] = ""

    response = client.post(
        "/api/v1/experiences",
        json=experience_payload,
    )

    assert response.status_code == 422


# =========================================================
# Update
# =========================================================


def test_update_experience(
    client: TestClient,
    experience: Experience,
):
    response = client.put(
        f"/api/v1/experiences/{experience.id}",
        json={
            "company": "Updated Company",
            "designation": "Senior Python Developer",
            "employment_type": "Full-time",
            "location": "Hyderabad",
            "location_type": "Remote",
            "start_date": "2024-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Updated backend responsibilities.",
            "display_order": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Experience updated successfully."
    assert body["data"]["company"] == "Updated Company"
    assert body["data"]["designation"] == "Senior Python Developer"
    assert body["data"]["display_order"] == 2


def test_update_missing_experience(
    client: TestClient,
    experience_payload: dict,
):
    response = client.put(
        "/api/v1/experiences/999999",
        json=experience_payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


def test_update_experience_with_duplicate_details(
    client: TestClient,
    experience: Experience,
    second_experience: Experience,
):
    response = client.put(
        f"/api/v1/experiences/{second_experience.id}",
        json={
            "company": experience.company,
            "designation": experience.designation,
            "employment_type": "Full-time",
            "location": "Hyderabad",
            "location_type": "Hybrid",
            "start_date": "2024-01-01",
            "end_date": None,
            "is_current": True,
            "description": "Duplicate details.",
            "display_order": 3,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "An experience with the same company, "
        "designation, and start date already exists."
    )


# =========================================================
# Delete
# =========================================================


def test_delete_experience(
    client: TestClient,
    experience: Experience,
):
    response = client.delete(
        f"/api/v1/experiences/{experience.id}"
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Experience deleted successfully."
    assert body["data"] is None

    get_response = client.get(
        f"/api/v1/experiences/{experience.id}"
    )
    assert get_response.status_code == 404


def test_delete_missing_experience(client: TestClient):
    response = client.delete("/api/v1/experiences/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


# =========================================================
# Experience-skill relationships
# =========================================================


def test_get_experience_skills_empty(
    client: TestClient,
    experience: Experience,
):
    response = client.get(
        f"/api/v1/experiences/{experience.id}/skills"
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Experience skills retrieved successfully."
    assert body["data"] == []


def test_get_skills_for_missing_experience(
    client: TestClient,
):
    response = client.get(
        "/api/v1/experiences/999999/skills"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


def test_add_skill_to_experience(
    client: TestClient,
    experience: Experience,
    skill: Skill,
):
    response = client.post(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == (
        "Skill associated with experience successfully."
    )

    skills_response = client.get(
        f"/api/v1/experiences/{experience.id}/skills"
    )

    assert skills_response.status_code == 200
    assert skills_response.json()["data"] == [skill.id]


def test_add_duplicate_skill_to_experience(
    client: TestClient,
    experience: Experience,
    skill: Skill,
):
    add_response = client.post(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )
    assert add_response.status_code == 200

    response = client.post(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Skill is already associated with this experience."
    )


def test_add_missing_skill_to_experience(
    client: TestClient,
    experience: Experience,
):
    response = client.post(
        f"/api/v1/experiences/{experience.id}/skills/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found."


def test_add_skill_to_missing_experience(
    client: TestClient,
    skill: Skill,
):
    response = client.post(
        f"/api/v1/experiences/999999/skills/{skill.id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


def test_replace_experience_skills(
    client: TestClient,
    experience: Experience,
    skill: Skill,
    second_skill: Skill,
):
    response = client.put(
        f"/api/v1/experiences/{experience.id}/skills",
        json={"skill_ids": [skill.id, second_skill.id]},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == (
        "Experience skills updated successfully."
    )

    skills_response = client.get(
        f"/api/v1/experiences/{experience.id}/skills"
    )

    assert skills_response.status_code == 200
    assert set(skills_response.json()["data"]) == {
        skill.id,
        second_skill.id,
    }


def test_replace_experience_skills_with_empty_list(
    client: TestClient,
    experience: Experience,
    skill: Skill,
):
    client.post(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )

    response = client.put(
        f"/api/v1/experiences/{experience.id}/skills",
        json={"skill_ids": []},
    )

    assert response.status_code == 200

    skills_response = client.get(
        f"/api/v1/experiences/{experience.id}/skills"
    )

    assert skills_response.json()["data"] == []


def test_replace_experience_skills_with_missing_skill(
    client: TestClient,
    experience: Experience,
):
    response = client.put(
        f"/api/v1/experiences/{experience.id}/skills",
        json={"skill_ids": [999999]},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found."


def test_replace_skills_for_missing_experience(
    client: TestClient,
    skill: Skill,
):
    response = client.put(
        "/api/v1/experiences/999999/skills",
        json={"skill_ids": [skill.id]},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


def test_remove_skill_from_experience(
    client: TestClient,
    experience: Experience,
    skill: Skill,
):
    client.post(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )

    response = client.delete(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == (
        "Skill removed from experience successfully."
    )

    skills_response = client.get(
        f"/api/v1/experiences/{experience.id}/skills"
    )

    assert skills_response.json()["data"] == []


def test_remove_unassociated_skill(
    client: TestClient,
    experience: Experience,
    skill: Skill,
):
    response = client.delete(
        f"/api/v1/experiences/{experience.id}/skills/{skill.id}"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Skill is not associated with this experience."
    )


def test_remove_missing_skill(
    client: TestClient,
    experience: Experience,
):
    response = client.delete(
        f"/api/v1/experiences/{experience.id}/skills/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found."


def test_invalid_skill_id_in_replacement_payload(
    client: TestClient,
    experience: Experience,
):
    response = client.put(
        f"/api/v1/experiences/{experience.id}/skills",
        json={"skill_ids": [0]},
    )

    assert response.status_code == 422