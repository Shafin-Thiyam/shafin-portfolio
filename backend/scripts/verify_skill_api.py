"""
Verify Skill API functionality.
"""

import sys

import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/skills"


def main() -> None:
    """
    Verify Skill API.
    """

    print("=" * 60)
    print("Skill API Verification")
    print("=" * 60)

    try:

        # ---------------------------------------------------------
        # Cleanup existing skills
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)
        response.raise_for_status()

        for skill in response.json()["data"]:
            requests.delete(f"{BASE_URL}/{skill['id']}")

        print("✓ Existing skills cleaned")

        # ---------------------------------------------------------
        # Create Skill
        # ---------------------------------------------------------

        payload = {
            "name": "Python",
            "category": "Backend",
            "proficiency": 95,
            "display_order": 1,
        }

        response = requests.post(
            BASE_URL,
            json=payload,
        )

        assert response.status_code == 201

        created = response.json()["data"]

        skill_id = created["id"]

        assert created["name"] == "Python"

        print("✓ POST /skills")

        # ---------------------------------------------------------
        # GET All
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200

        skills = response.json()["data"]

        assert len(skills) == 1

        print("✓ GET /skills")

        # ---------------------------------------------------------
        # GET by ID
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{skill_id}"
        )

        assert response.status_code == 200

        assert response.json()["data"]["id"] == skill_id

        print("✓ GET /skills/{id}")

        # ---------------------------------------------------------
        # GET by Category
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={
                "category": "Backend",
            },
        )

        assert response.status_code == 200

        skills = response.json()["data"]

        assert len(skills) == 1

        print("✓ GET /skills?category=")

        # ---------------------------------------------------------
        # Update Skill
        # ---------------------------------------------------------

        update = {
            "name": "FastAPI",
            "category": "Backend",
            "proficiency": 98,
            "display_order": 2,
        }

        response = requests.put(
            f"{BASE_URL}/{skill_id}",
            json=update,
        )

        assert response.status_code == 200

        assert response.json()["data"]["name"] == "FastAPI"

        print("✓ PUT /skills/{id}")

        # ---------------------------------------------------------
        # Verify persisted update
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{skill_id}"
        )

        assert response.status_code == 200

        assert response.json()["data"]["name"] == "FastAPI"

        print("✓ Updated values verified")

        # ---------------------------------------------------------
        # Delete
        # ---------------------------------------------------------

        response = requests.delete(
            f"{BASE_URL}/{skill_id}"
        )

        assert response.status_code == 200

        print("✓ DELETE /skills/{id}")

        # ---------------------------------------------------------
        # Verify deletion
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{skill_id}"
        )

        assert response.status_code == 404

        print("✓ Deletion verified")
        
        # ---------------------------------------------------------
        # GET Missing Skill
        # ---------------------------------------------------------

        response = requests.get(f"{BASE_URL}/999999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found."

        print("✓ GET missing skill")

        # ---------------------------------------------------------
        # Create base skill for remaining tests
        # ---------------------------------------------------------

        python_payload = {
            "name": "Python",
            "category": "Backend",
            "proficiency": 95,
            "display_order": 1,
        }

        response = requests.post(
            BASE_URL,
            json=python_payload,
        )

        assert response.status_code == 201

        python_id = response.json()["data"]["id"]

        # ---------------------------------------------------------
        # POST Duplicate Skill
        # ---------------------------------------------------------

        response = requests.post(
            BASE_URL,
            json=python_payload,
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "Skill already exists."

        print("✓ POST duplicate skill")

        # ---------------------------------------------------------
        # PUT Missing Skill
        # ---------------------------------------------------------

        response = requests.put(
            f"{BASE_URL}/999999",
            json={
                "name": "FastAPI",
                "category": "Backend",
                "proficiency": 98,
                "display_order": 2,
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found."

        print("✓ PUT missing skill")

        # ---------------------------------------------------------
        # Create second skill
        # ---------------------------------------------------------

        docker_payload = {
            "name": "Docker",
            "category": "DevOps",
            "proficiency": 90,
            "display_order": 2,
        }

        response = requests.post(
            BASE_URL,
            json=docker_payload,
        )

        assert response.status_code == 201

        docker_id = response.json()["data"]["id"]

        # ---------------------------------------------------------
        # PUT Duplicate Name
        # ---------------------------------------------------------

        response = requests.put(
            f"{BASE_URL}/{docker_id}",
            json={
                "name": "Python",
                "category": "DevOps",
                "proficiency": 90,
                "display_order": 2,
            },
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "Skill already exists."

        print("✓ PUT duplicate name")

        # ---------------------------------------------------------
        # DELETE Missing Skill
        # ---------------------------------------------------------

        response = requests.delete(f"{BASE_URL}/999999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found."

        print("✓ DELETE missing skill")

        # ---------------------------------------------------------
        # Empty Name Validation
        # ---------------------------------------------------------

        response = requests.post(
            BASE_URL,
            json={
                "name": "",
                "category": "Backend",
                "proficiency": 95,
                "display_order": 1,
            },
        )

        assert response.status_code == 422

        print("✓ Empty name validation")

        # ---------------------------------------------------------
        # Proficiency Validation
        # ---------------------------------------------------------

        response = requests.post(
            BASE_URL,
            json={
                "name": "Kubernetes",
                "category": "DevOps",
                "proficiency": 120,
                "display_order": 3,
            },
        )

        assert response.status_code == 422

        print("✓ Proficiency validation")

        # ---------------------------------------------------------
        # Negative Display Order Validation
        # ---------------------------------------------------------

        response = requests.post(
            BASE_URL,
            json={
                "name": "Kafka",
                "category": "Backend",
                "proficiency": 90,
                "display_order": -1,
            },
        )

        assert response.status_code == 422

        print("✓ Negative display order validation")

        print()
        print("=" * 60)
        print("API Verification Summary")
        print("=" * 60)

        print("✓ POST")
        print("✓ GET")
        print("✓ GET by ID")
        print("✓ GET by Category")
        print("✓ PUT")
        print("✓ DELETE")
        print("✓ Persistence verified")

        print()
        print("🎉 Skill API verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ API verification failed")
        print(exc)
        sys.exit(1)

    except requests.RequestException as exc:

        print()
        print("❌ HTTP request failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    print("=" * 60)
    print("API verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()