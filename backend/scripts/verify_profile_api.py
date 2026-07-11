"""
Verify Profile API.
"""

import sys

import requests
import uuid


BASE_URL = "http://127.0.0.1:8000/api/v1"
EXPECTED_NAME = "Shafin Thiyam"

EXPECTED_EMAIL = f"{uuid.uuid4()}@example.com"
#EXPECTED_EMAIL = "shafin@example.com"

def api_url(path: str) -> str:
    """
    Build API URL.
    """
    return f"{BASE_URL}{path}"

def profile_payload() -> dict:
    """
    Sample profile payload.
    """

    return {
        "full_name": EXPECTED_NAME,
        "title": "Associate Consultant",
        "email": EXPECTED_EMAIL,
        "phone": "+91-9876543210",
        "location": "Hyderabad, India",
        "linkedin_url": "https://linkedin.com/in/shafin",
        "github_url": "https://github.com/Shafin-Thiyam",
        "portfolio_url": "https://shafin.dev",
        "summary": "Python Backend Developer",
        "profile_image": None,
        "resume_url": None,
    }

def profile_update_payload() -> dict:
    """
    Updated profile payload.
    """

    return {
        "full_name": EXPECTED_NAME,
        "title": "Senior Associate Consultant",
        "email": EXPECTED_EMAIL,
        "phone": "+91-9000000000",
        "location": "Bengaluru, India",
        "linkedin_url": "https://linkedin.com/in/shafin",
        "github_url": "https://github.com/Shafin-Thiyam",
        "portfolio_url": "https://shafin.dev",
        "summary": "Senior Python Backend Developer",
        "profile_image": None,
        "resume_url": None,
    }

def cleanup_profile() -> None:
    """
    Remove any existing profile before testing.
    """

    response = requests.delete(api_url("/profile"))

    if response.status_code not in (200, 404):
        raise AssertionError(
            f"Unexpected cleanup status: {response.status_code}"
        )

    print("✓ Existing profile cleaned")
    
def verify_delete_profile() -> None:
    pass
       
def verify_get_profile() -> None:
    """
    Verify GET /profile.
    """

    print("-" * 60)
    print("Verify GET /profile")
    print("-" * 60)
    
    response = requests.get(api_url("/profile"),)
    
    assert response.status_code == 200

    print("✓ Status code")

    payload = response.json()

    assert payload["success"] is True

    print("✓ success")

    assert (
        payload["message"]
        == "Profile retrieved successfully."
    )

    print("✓ message")

    assert payload["data"] is not None

    print("✓ data returned")

    data = payload["data"]

    assert data["id"] > 0
    assert data["full_name"] == EXPECTED_NAME
    assert data["email"] == EXPECTED_EMAIL

    print("✓ profile fields")
    
def verify_post_profile() -> None:
    """
    Verify POST /profile.
    """

    print("-" * 60)
    print("Verify POST /profile")
    print("-" * 60)

    response = requests.post(
        api_url("/profile"),
        json=profile_payload(),
    )
    
    assert response.status_code == 201

    print("✓ Status code")
    
    payload = response.json()

    assert payload["success"] is True

    print("✓ success")
    
    assert (
        payload["message"]
        == "Profile created successfully."
    )

    print("✓ message")
    
    data = payload["data"]

    assert data is not None

    assert data["id"] > 0
    assert data["full_name"] == EXPECTED_NAME
    assert data["email"] == EXPECTED_EMAIL

    print("✓ profile created")
    
    response = requests.get(api_url("/profile"))

    assert response.status_code == 200

    payload = response.json()

    assert payload["data"]["email"] == EXPECTED_EMAIL

    print("✓ profile persisted")

def verify_put_profile() -> None:
    """
    Verify PUT /profile.
    """

    print("-" * 60)
    print("Verify PUT /profile")
    print("-" * 60)

    response = requests.put(
        api_url("/profile"),
        json=profile_update_payload(),
    )

    assert response.status_code == 200

    print("✓ Status code")

    payload = response.json()

    assert payload["success"] is True

    print("✓ success")

    assert (
        payload["message"]
        == "Profile updated successfully."
    )

    print("✓ message")

    data = payload["data"]

    assert data is not None

    assert (
        data["title"]
        == "Senior Associate Consultant"
    )

    assert (
        data["location"]
        == "Bengaluru, India"
    )

    assert (
        data["summary"]
        == "Senior Python Backend Developer"
    )

    print("✓ response updated")

    response = requests.get(
        api_url("/profile")
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert (
        data["title"]
        == "Senior Associate Consultant"
    )

    assert (
        data["location"]
        == "Bengaluru, India"
    )

    assert (
        data["summary"]
        == "Senior Python Backend Developer"
    )

    print("✓ update persisted")

def verify_delete_profile() -> None:
    """
    Verify DELETE /profile.
    """

    print("-" * 60)
    print("Verify DELETE /profile")
    print("-" * 60)

    response = requests.delete(
        api_url("/profile")
    )

    assert response.status_code == 200

    print("✓ Status code")

    payload = response.json()

    assert payload["success"] is True

    print("✓ success")

    assert (
        payload["message"]
        == "Profile deleted successfully."
    )

    print("✓ message")

    assert payload["data"] is None

    print("✓ response data")

    # ---------------------------------------------------------
    # Verify profile no longer exists
    # ---------------------------------------------------------

    response = requests.get(
        api_url("/profile")
    )

    assert response.status_code == 404

    print("✓ GET returns 404")

    payload = response.json()

    assert (
        payload["detail"]
        == "Profile not found."
    )

    print("✓ profile removed")

def verify_get_profile_not_found() -> None:
    """
    Verify GET /profile when no profile exists.
    """

    print("-" * 60)
    print("Verify GET /profile (404)")
    print("-" * 60)

    cleanup_profile()

    response = requests.get(
        api_url("/profile")
    )

    assert response.status_code == 404

    payload = response.json()

    assert (
        payload["detail"]
        == "Profile not found."
    )

    print("✓ GET returns 404")
    
def verify_put_profile_not_found() -> None:
    """
    Verify PUT /profile when no profile exists.
    """

    print("-" * 60)
    print("Verify PUT /profile (404)")
    print("-" * 60)

    cleanup_profile()

    response = requests.put(
        api_url("/profile"),
        json=profile_update_payload(),
    )

    assert response.status_code == 404

    payload = response.json()

    assert (
        payload["detail"]
        == "Profile not found."
    )

    print("✓ PUT returns 404")
    
def verify_delete_profile_not_found() -> None:
    """
    Verify DELETE /profile when no profile exists.
    """

    print("-" * 60)
    print("Verify DELETE /profile (404)")
    print("-" * 60)

    cleanup_profile()

    response = requests.delete(
        api_url("/profile")
    )

    assert response.status_code == 404

    payload = response.json()

    assert (
        payload["detail"]
        == "Profile not found."
    )

    print("✓ DELETE returns 404")
    
def verify_post_invalid_payload() -> None:
    """
    Verify POST validation.
    """

    print("-" * 60)
    print("Verify POST validation")
    print("-" * 60)

    payload = profile_payload()

    del payload["email"]

    response = requests.post(
        api_url("/profile"),
        json=payload,
    )

    assert response.status_code == 422

    print("✓ Validation error")

def verify_put_invalid_payload() -> None:
    """
    Verify PUT validation.
    """

    print("-" * 60)
    print("Verify PUT validation")
    print("-" * 60)

    payload = profile_update_payload()

    del payload["title"]

    response = requests.put(
        api_url("/profile"),
        json=payload,
    )

    assert response.status_code == 422

    print("✓ Validation error")

def main() -> None:
    print("=" * 60)
    print("Profile API Verification")
    print("=" * 60)
    
    cleanup_profile()

    verify_get_profile_not_found()
    verify_put_profile_not_found()
    verify_delete_profile_not_found()

    verify_post_profile()
    verify_get_profile()
    verify_put_profile()
    verify_delete_profile()    
    print()
    
    verify_post_invalid_payload()
    verify_put_invalid_payload()

    print("=" * 60)
    print("Profile API Verification Summary")
    print("=" * 60)

    print("✓ POST /profile")
    print("✓ GET /profile")
    print("✓ PUT /profile")
    print("✓ DELETE /profile")

    print()
    print("🎉 API verification completed successfully.")
    print("=" * 60)



if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print()
        print("❌ API verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:
        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)