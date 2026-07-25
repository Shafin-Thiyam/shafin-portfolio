"""
Verify Education API endpoints.
"""

import sys
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/education"
DOCS_URL = "http://127.0.0.1:8000/openapi.json"


def main() -> None:
    """
    Verify Education API.
    """

    print("=" * 60)
    print("Education API Verification")
    print("=" * 60)

    try:

        # ---------------------------------------------------------
        # FastAPI Started
        # ---------------------------------------------------------

        openapi_response = requests.get(DOCS_URL)
        openapi_response.raise_for_status()
        
        openapi = openapi_response.json()

        print("✓ FastAPI started")

        # ---------------------------------------------------------
        # Router Registered
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200

        print("✓ Router registered")

        # ---------------------------------------------------------
        # OpenAPI Verification
        # ---------------------------------------------------------

        #openapi = response.json()

        paths = openapi["paths"]

        assert "/api/v1/education" in paths
        assert "/api/v1/education/{education_id}" in paths

        print("✓ OpenAPI verified")

        # ---------------------------------------------------------
        # GET /education
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200

        body = response.json()

        assert body["success"] is True
        assert "data" in body

        print("✓ GET /education")

        # ---------------------------------------------------------
        # POST /education
        # ---------------------------------------------------------

        payload = {
            "institution": "API Test University",
            "degree": "Bachelor of Engineering",
            "field_of_study": "Computer Science",
            "start_date": "2015-08-01",
            "end_date": "2019-05-31",
            "grade": "8.8 CGPA",
            "description": "API verification record.",
            "display_order": 999,
        }

        response = requests.post(
            BASE_URL,
            json=payload,
        )

        assert response.status_code == 201

        created = response.json()["data"]

        education_id = created["id"]

        print("✓ POST /education")

        # ---------------------------------------------------------
        # GET /education/{id}
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{education_id}"
        )

        assert response.status_code == 200

        assert (
            response.json()["data"]["id"]
            == education_id
        )

        print("✓ GET /education/{id}")

        # ---------------------------------------------------------
        # PUT /education/{id}
        # ---------------------------------------------------------

        update = {
            "institution": "Updated API University",
            "degree": "Master of Technology",
            "field_of_study": "Software Engineering",
            "start_date": "2020-08-01",
            "end_date": "2022-05-31",
            "grade": "9.5 CGPA",
            "description": "Updated via API.",
            "display_order": 1,
        }

        response = requests.put(
            f"{BASE_URL}/{education_id}",
            json=update,
        )

        assert response.status_code == 200

        assert (
            response.json()["data"]["institution"]
            == "Updated API University"
        )

        print("✓ PUT /education/{id}")

        # ---------------------------------------------------------
        # DELETE /education/{id}
        # ---------------------------------------------------------

        response = requests.delete(
            f"{BASE_URL}/{education_id}"
        )

        assert response.status_code == 200
        
        response = requests.get(
            f"{BASE_URL}/{education_id}"
        )

        assert response.status_code == 404

        print("✓ DELETE /education/{id}")

        # ---------------------------------------------------------
        # Degree Filter
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={
                "degree": "Bachelor of Engineering",
            },
        )

        assert response.status_code == 200
        
        body = response.json()

        assert body["success"] is True
        assert "data" in body

        print("✓ Degree filter")

        # ---------------------------------------------------------
        # Field of Study Filter
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={
                "field_of_study": "Computer Science",
            },
        )

        assert response.status_code == 200

        print("✓ Field of study filter")

        # ---------------------------------------------------------
        # OpenAPI Schema
        # ---------------------------------------------------------

        get_operation = openapi["paths"]["/api/v1/education"]["get"]

        response_schema = (
            get_operation["responses"]["200"]["content"]
            ["application/json"]["schema"]
        )

        assert response_schema["$ref"].startswith(
            "#/components/schemas/"
        )

        print("✓ OpenAPI schema")

        print()
        print("=" * 60)
        print("API Verification Summary")
        print("=" * 60)

        print("✓ Router registration")
        print("✓ CRUD endpoints")
        print("✓ Query filters")
        print("✓ OpenAPI schema")

        print()
        print("🎉 Education API verified successfully.")

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