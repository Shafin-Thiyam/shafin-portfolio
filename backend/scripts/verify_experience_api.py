
"""
Verify Experience API endpoints and experience-skill relationships.

Run from backend:
    python -m scripts.verify_experience_api

The verifier uses dedicated test records and existing skills.
It does not delete or modify seeded portfolio experiences or skills.
"""

import sys
from uuid import uuid4

import requests


BASE_URL = "http://127.0.0.1:8000/api/v1/experiences"
SKILLS_URL = "http://127.0.0.1:8000/api/v1/skills"
DOCS_URL = "http://127.0.0.1:8000/openapi.json"
TIMEOUT = 10

created_experience_ids: list[int] = []


def check_status(
    response: requests.Response,
    expected_status: int,
    operation: str,
) -> requests.Response:
    """Validate an HTTP status and include the response body on failure."""

    assert response.status_code == expected_status, (
        f"{operation}: expected HTTP {expected_status}, "
        f"got HTTP {response.status_code}. "
        f"Response: {response.text[:1500]}"
    )

    return response


def check_success_envelope(
    response: requests.Response,
    operation: str,
) -> dict:
    """Validate the common successful API response envelope."""

    body = response.json()

    assert body.get("success") is True, (
        f"{operation}: expected success=True; response={body}"
    )
    assert "message" in body, (
        f"{operation}: missing message; response={body}"
    )
    assert "data" in body, (
        f"{operation}: missing data; response={body}"
    )

    return body


def experience_payload(
    company: str,
    designation: str,
    display_order: int,
    *,
    is_current: bool = False,
) -> dict:
    """Create a valid, uniquely identifiable experience payload."""

    return {
        "company": company,
        "designation": designation,
        "employment_type": "Full-time",
        "location": "Hyderabad",
        "location_type": "Remote",
        "start_date": "2001-01-01",
        "end_date": None if is_current else "2002-01-01",
        "is_current": is_current,
        "description": "Temporary Experience API verification record.",
        "display_order": display_order,
    }


def create_test_experience(payload: dict) -> dict:
    """Create a test experience and register it for cleanup."""

    response = requests.post(
        BASE_URL,
        json=payload,
        timeout=TIMEOUT,
    )
    check_status(response, 201, "POST /experiences")

    body = check_success_envelope(response, "POST /experiences")
    created = body["data"]

    assert isinstance(created.get("id"), int), (
        f"Created experience has no valid ID: {created}"
    )

    created_experience_ids.append(created["id"])
    return created


def main() -> None:
    """Verify Experience API behavior."""

    print("=" * 60)
    print("Experience API Verification")
    print("=" * 60)

    # Use unique names to avoid collisions with existing portfolio data.
    token = uuid4().hex[:12]
    company = f"API Verification {token}"
    duplicate_company = f"API Duplicate {token}"

    primary_id = None
    current_id = None
    duplicate_id = None

    try:
        # ---------------------------------------------------------
        # 1. Application and OpenAPI
        # ---------------------------------------------------------

        response = requests.get(DOCS_URL, timeout=TIMEOUT)
        check_status(response, 200, "GET /openapi.json")
        openapi = response.json()

        print("✓ FastAPI started")

        response = requests.get(BASE_URL, timeout=TIMEOUT)
        check_status(response, 200, "GET /experiences")
        check_success_envelope(response, "GET /experiences")

        print("✓ Experience router registered")

        paths = openapi["paths"]

        expected_methods = {
            "/api/v1/experiences": {"get", "post"},
            "/api/v1/experiences/current": {"get"},
            "/api/v1/experiences/{experience_id}": {
                "get", "put", "delete"
            },
            "/api/v1/experiences/{experience_id}/skills": {
                "get", "put"
            },
            "/api/v1/experiences/{experience_id}/skills/{skill_id}": {
                "post", "delete"
            },
        }

        for path, methods in expected_methods.items():
            assert path in paths, f"Missing OpenAPI path: {path}"

            actual_methods = set(paths[path])
            assert methods.issubset(actual_methods), (
                f"{path}: expected methods {methods}, "
                f"found {actual_methods}"
            )

        print("✓ OpenAPI paths and methods")

        # ---------------------------------------------------------
        # 2. Discover existing skills without modifying them
        # ---------------------------------------------------------

        response = requests.get(SKILLS_URL, timeout=TIMEOUT)
        check_status(response, 200, "GET /skills")

        skills_body = check_success_envelope(response, "GET /skills")
        skills = skills_body["data"]

        skills_by_name = {
            skill["name"].casefold(): skill["id"]
            for skill in skills
        }

        assert "python" in skills_by_name, (
            "The existing Skills API must contain Python."
        )
        assert "fastapi" in skills_by_name, (
            "The existing Skills API must contain FastAPI."
        )

        python_id = skills_by_name["python"]
        fastapi_id = skills_by_name["fastapi"]

        existing_skill_ids = [
            skill["id"] for skill in skills
        ]

        missing_skill_id = max(existing_skill_ids, default=0) + 100000

        print("✓ Existing skills discovered")

        # ---------------------------------------------------------
        # 3. Create and retrieve an experience
        # ---------------------------------------------------------

        payload = experience_payload(
            company,
            "API Verification Engineer",
            900001,
        )

        created = create_test_experience(payload)
        primary_id = created["id"]

        assert created["company"] == company
        assert created["designation"] == "API Verification Engineer"
        assert created["is_current"] is False

        print("✓ POST /experiences")

        response = requests.get(
            BASE_URL,
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET /experiences")

        body = check_success_envelope(response, "GET /experiences")
        assert any(item["id"] == primary_id for item in body["data"])

        print("✓ GET /experiences")

        response = requests.get(
            f"{BASE_URL}/{primary_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET /experiences/{id}")

        body = check_success_envelope(
            response,
            "GET /experiences/{id}",
        )
        assert body["data"]["id"] == primary_id

        print("✓ GET /experiences/{id}")

        # ---------------------------------------------------------
        # 4. Update and verify persistence
        # ---------------------------------------------------------

        update_payload = experience_payload(
            company,
            "Updated API Verification Engineer",
            900002,
        )

        response = requests.put(
            f"{BASE_URL}/{primary_id}",
            json=update_payload,
            timeout=TIMEOUT,
        )
        check_status(response, 200, "PUT /experiences/{id}")

        body = check_success_envelope(
            response,
            "PUT /experiences/{id}",
        )
        assert (
            body["data"]["designation"]
            == "Updated API Verification Engineer"
        )

        response = requests.get(
            f"{BASE_URL}/{primary_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET updated experience")

        body = check_success_envelope(
            response,
            "GET updated experience",
        )
        assert (
            body["data"]["designation"]
            == "Updated API Verification Engineer"
        )

        print("✓ PUT /experiences/{id} and persisted update")

        # ---------------------------------------------------------
        # 5. Collection filters
        # ---------------------------------------------------------

        for parameter, value in (
            ("company", company),
            ("employment_type", "full-time"),
            ("location_type", "remote"),
        ):
            response = requests.get(
                BASE_URL,
                params={parameter: value},
                timeout=TIMEOUT,
            )
            check_status(
                response,
                200,
                f"GET /experiences?{parameter}=",
            )

            body = check_success_envelope(
                response,
                f"{parameter} filter",
            )

            if parameter == "company":
                assert any(
                    item["id"] == primary_id
                    for item in body["data"]
                )
                assert all(
                    company.casefold() in item["company"].casefold()
                    for item in body["data"]
                )
            elif parameter == "employment_type":
                assert all(
                    item["employment_type"].casefold() == "full-time"
                    for item in body["data"]
                )
            else:
                assert all(
                    item["location_type"].casefold() == "remote"
                    for item in body["data"]
                )

            print(f"✓ {parameter} filter")

        # ---------------------------------------------------------
        # 6. Current experiences
        # ---------------------------------------------------------

        current_payload = experience_payload(
            company,
            "Current API Verification Engineer",
            900003,
            is_current=True,
        )

        current = create_test_experience(current_payload)
        current_id = current["id"]

        response = requests.get(
            f"{BASE_URL}/current",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET /experiences/current")

        body = check_success_envelope(
            response,
            "GET /experiences/current",
        )

        assert all(item["is_current"] for item in body["data"])
        assert any(
            item["id"] == current_id for item in body["data"]
        )

        print("✓ GET /experiences/current")

        # ---------------------------------------------------------
        # 7. Experience-skill relationships
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{primary_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET experience skills")

        body = check_success_envelope(
            response,
            "GET experience skills",
        )
        assert body["data"] == []

        print("✓ GET /experiences/{id}/skills")

        response = requests.post(
            f"{BASE_URL}/{primary_id}/skills/{python_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "POST experience skill")
        check_success_envelope(response, "POST experience skill")

        response = requests.get(
            f"{BASE_URL}/{primary_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET associated skills")

        body = check_success_envelope(
            response,
            "GET associated skills",
        )
        assert python_id in body["data"]

        print("✓ POST skill association")

        # Duplicate association must not silently succeed.
        response = requests.post(
            f"{BASE_URL}/{primary_id}/skills/{python_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 409, "POST duplicate experience skill")

        print("✓ Duplicate skill association returns 409")

        response = requests.put(
            f"{BASE_URL}/{primary_id}/skills",
            json={"skill_ids": [python_id, fastapi_id]},
            timeout=TIMEOUT,
        )
        check_status(response, 200, "PUT experience skills")
        check_success_envelope(response, "PUT experience skills")

        response = requests.get(
            f"{BASE_URL}/{primary_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET replaced skills")

        body = check_success_envelope(
            response,
            "GET replaced skills",
        )
        assert set(body["data"]) == {python_id, fastapi_id}

        print("✓ PUT replaces skill associations")

        # Invalid replacement must preserve existing associations.
        response = requests.put(
            f"{BASE_URL}/{primary_id}/skills",
            json={"skill_ids": [missing_skill_id]},
            timeout=TIMEOUT,
        )
        check_status(response, 404, "PUT with missing skill")

        response = requests.get(
            f"{BASE_URL}/{primary_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET skills after failed replacement")

        body = check_success_envelope(
            response,
            "GET skills after failed replacement",
        )
        assert set(body["data"]) == {python_id, fastapi_id}

        print("✓ Failed skill replacement preserves associations")

        response = requests.delete(
            f"{BASE_URL}/{primary_id}/skills/{fastapi_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "DELETE experience skill")
        check_success_envelope(response, "DELETE experience skill")

        response = requests.get(
            f"{BASE_URL}/{primary_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET skills after removal")

        body = check_success_envelope(
            response,
            "GET skills after removal",
        )
        assert body["data"] == [python_id]

        print("✓ DELETE skill association")

        # Empty list should clear all associations.
        response = requests.put(
            f"{BASE_URL}/{primary_id}/skills",
            json={"skill_ids": []},
            timeout=TIMEOUT,
        )
        check_status(response, 200, "PUT empty skill list")
        check_success_envelope(response, "PUT empty skill list")

        response = requests.get(
            f"{BASE_URL}/{primary_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "GET cleared skills")

        body = check_success_envelope(
            response,
            "GET cleared skills",
        )
        assert body["data"] == []

        print("✓ Empty skill list clears associations")

        # ---------------------------------------------------------
        # 8. Missing resources
        # ---------------------------------------------------------

        missing_experience_id = 99999999

        response = requests.get(
            f"{BASE_URL}/{missing_experience_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 404, "GET missing experience")

        response = requests.put(
            f"{BASE_URL}/{missing_experience_id}",
            json=update_payload,
            timeout=TIMEOUT,
        )
        check_status(response, 404, "PUT missing experience")

        response = requests.delete(
            f"{BASE_URL}/{missing_experience_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 404, "DELETE missing experience")

        response = requests.get(
            f"{BASE_URL}/{missing_experience_id}/skills",
            timeout=TIMEOUT,
        )
        check_status(response, 404, "GET skills for missing experience")

        response = requests.post(
            f"{BASE_URL}/{missing_experience_id}/skills/{python_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 404, "POST skill for missing experience")

        print("✓ Missing experience returns 404")

        response = requests.post(
            f"{BASE_URL}/{primary_id}/skills/{missing_skill_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 404, "POST missing skill")

        print("✓ Missing skill returns 404")

        # Removing a skill that is not associated must return 409.
        response = requests.delete(
            f"{BASE_URL}/{primary_id}/skills/{fastapi_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 409, "DELETE unassociated skill")

        print("✓ Removing an unassociated skill returns 409")

        # ---------------------------------------------------------
        # 9. Duplicate experience and payload validation
        # ---------------------------------------------------------

        duplicate_payload = experience_payload(
            duplicate_company,
            "Duplicate Verification Engineer",
            900004,
        )

        duplicate = create_test_experience(duplicate_payload)
        duplicate_id = duplicate["id"]

        response = requests.post(
            BASE_URL,
            json=duplicate_payload,
            timeout=TIMEOUT,
        )
        check_status(response, 409, "POST duplicate experience")

        print("✓ Duplicate experience returns 409")

        invalid_payload = dict(payload)
        invalid_payload["company"] = ""
        invalid_payload["display_order"] = -1

        response = requests.post(
            BASE_URL,
            json=invalid_payload,
            timeout=TIMEOUT,
        )
        check_status(response, 422, "POST invalid experience")

        print("✓ Invalid payload returns 422")

        # ---------------------------------------------------------
        # 10. Delete and verify deletion
        # ---------------------------------------------------------

        response = requests.delete(
            f"{BASE_URL}/{duplicate_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "DELETE experience")

        body = check_success_envelope(response, "DELETE experience")
        assert body["data"] is None

        created_experience_ids.remove(duplicate_id)
        duplicate_id = None

        response = requests.get(
            f"{BASE_URL}/{primary_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "Verify remaining experience")

        response = requests.delete(
            f"{BASE_URL}/{primary_id}",
            timeout=TIMEOUT,
        )
        check_status(response, 200, "DELETE primary experience")

        created_experience_ids.remove(primary_id)
        primary_id = None

        response = requests.get(
            f"{BASE_URL}/{primary_id or 99999999}",
            timeout=TIMEOUT,
        )
        check_status(response, 404, "Verify deleted experience")

        print("✓ DELETE experience and verify deletion")

        print()
        print("=" * 60)
        print("Experience API Verification Summary")
        print("=" * 60)
        print("✓ Application and OpenAPI")
        print("✓ Experience CRUD")
        print("✓ Collection filters")
        print("✓ Current experiences")
        print("✓ Skill relationship endpoints")
        print("✓ Invalid and missing resources")
        print("✓ Duplicate and payload validation")
        print("✓ Failed replacement preserves associations")
        print("✓ Deletion")

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
        print(f"{type(exc).__name__}: {exc}")
        sys.exit(1)

    finally:
        # Clean up only records created by this verifier.
        for experience_id in reversed(created_experience_ids):
            try:
                requests.delete(
                    f"{BASE_URL}/{experience_id}",
                    timeout=TIMEOUT,
                )
            except requests.RequestException:
                print(
                    "⚠️ Could not clean up test experience "
                    f"{experience_id}"
                )

    print()
    print("🎉 Experience API verification passed.")
    print("Experience API verification completed.")


if __name__ == "__main__":
    main()
