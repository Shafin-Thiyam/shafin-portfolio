"""Integration tests for the Project API."""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Experience, Project


@pytest.fixture
def experience(db_session: Session) -> Experience:
    """Create an experience used by project tests."""

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
def project_payload(experience: Experience) -> dict:
    """Return a valid project creation payload."""

    return {
        "experience_id": experience.id,
        "title": "Portfolio API",
        "description": "A portfolio backend built with FastAPI.",
        "role": "Backend Developer",
        "technologies": ["Python", "FastAPI", "PostgreSQL"],
        "project_url": "https://example.com",
        "repository_url": "https://github.com/example/portfolio",
        "start_date": "2025-01-01",
        "end_date": "2025-03-31",
        "display_order": 1,
    }


@pytest.fixture
def project(
    db_session: Session,
    experience: Experience,
) -> Project:
    """Create a project directly in the test database."""

    item = Project(
        experience_id=experience.id,
        title="Existing Project",
        description="An existing test project.",
        role="Developer",
        technologies=["Python"],
        project_url=None,
        repository_url=None,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 2, 1),
        display_order=1,
    )

    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    return item


def test_list_projects_empty(client: TestClient):
    response = client.get("/api/v1/projects")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Projects retrieved successfully."
    assert body["data"] == []


def test_create_project(
    client: TestClient,
    project_payload: dict,
):
    response = client.post(
        "/api/v1/projects",
        json=project_payload,
    )

    assert response.status_code == 201

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Project created successfully."
    assert body["data"]["title"] == "Portfolio API"
    assert body["data"]["technologies"] == [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]
    assert body["data"]["experience_id"] == project_payload["experience_id"]
    assert body["data"]["id"] is not None


def test_list_projects(
    client: TestClient,
    project: Project,
):
    response = client.get("/api/v1/projects")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == project.id
    assert body["data"][0]["title"] == "Existing Project"


def test_get_project_by_id(
    client: TestClient,
    project: Project,
):
    response = client.get(f"/api/v1/projects/{project.id}")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Project retrieved successfully."
    assert body["data"]["id"] == project.id
    assert body["data"]["title"] == "Existing Project"


def test_get_missing_project(client: TestClient):
    response = client.get("/api/v1/projects/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found."


def test_create_project_for_missing_experience(
    client: TestClient,
    project_payload: dict,
):
    project_payload["experience_id"] = 999999

    response = client.post(
        "/api/v1/projects",
        json=project_payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


def test_update_project(
    client: TestClient,
    project: Project,
):
    response = client.put(
        f"/api/v1/projects/{project.id}",
        json={
            "experience_id": project.experience_id,
            "title": "Updated Project",
            "description": "Updated description.",
            "role": "Senior Developer",
            "technologies": ["Python", "FastAPI"],
            "project_url": None,
            "repository_url": None,
            "start_date": "2025-01-01",
            "end_date": "2025-04-01",
            "display_order": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Project updated successfully."
    assert body["data"]["title"] == "Updated Project"
    assert body["data"]["display_order"] == 2


def test_update_missing_project(
    client: TestClient,
    project_payload: dict,
):
    response = client.put(
        "/api/v1/projects/999999",
        json=project_payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found."

def test_update_project_missing_required_field(
    client: TestClient,
    project: Project,
):
    response = client.put(
        f"/api/v1/projects/{project.id}",
        json={
            "experience_id": 999999,
            "title": "Updated Project",
            "description": None,
            "role": None,
            "project_url": None,
            "repository_url": None,
            "start_date": None,
            "end_date": None,
            "display_order": 0,
        },
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "technologies"]
        and error["type"] == "missing"
        for error in detail
    )


def test_update_project_with_missing_experience(
    client: TestClient,
    project: Project,
):
    response = client.put(
        f"/api/v1/projects/{project.id}",
        json={
            "experience_id": 999999,
            "title": "Updated Project",
            "description": None,
            "role": None,
            "technologies": [],
            "project_url": None,
            "repository_url": None,
            "start_date": None,
            "end_date": None,
            "display_order": 0,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."




def test_delete_project(
    client: TestClient,
    project: Project,
):
    response = client.delete(f"/api/v1/projects/{project.id}")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Project deleted successfully."
    assert body["data"] is None

    get_response = client.get(f"/api/v1/projects/{project.id}")
    assert get_response.status_code == 404


def test_delete_missing_project(client: TestClient):
    response = client.delete("/api/v1/projects/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found."


def test_get_projects_by_experience(
    client: TestClient,
    experience: Experience,
    project: Project,
):
    response = client.get(
        f"/api/v1/experiences/{experience.id}/projects"
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == (
        "Experience projects retrieved successfully."
    )
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == project.id


def test_get_projects_for_missing_experience(
    client: TestClient,
):
    response = client.get(
        "/api/v1/experiences/999999/projects"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Experience not found."


def test_create_project_with_invalid_data(
    client: TestClient,
    project_payload: dict,
):
    project_payload["title"] = ""

    response = client.post(
        "/api/v1/projects",
        json=project_payload,
    )

    assert response.status_code == 422
