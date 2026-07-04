"""
Verify Profile schemas.
"""

import sys
from datetime import datetime, UTC

from app.models import Profile
from app.schemas import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)


def main() -> None:
    """
    Verify Profile schemas.
    """

    print("=" * 60)
    print("Profile Schema Verification")
    print("=" * 60)

    try:

        # ---------------------------------------------------------
        # ProfileCreate
        # ---------------------------------------------------------

        create_schema = ProfileCreate(
            full_name="Shafin Thiyam",
            title="Associate Consultant",
            email="shafin@example.com",
            phone="+91-9876543210",
            location="Hyderabad",
            linkedin_url="https://linkedin.com/in/shafin",
            github_url="https://github.com/Shafin-Thiyam",
            portfolio_url="https://portfolio.example.com",
            summary="Python Backend Developer",
            profile_image=None,
            resume_url=None,
        )

        print("✓ ProfileCreate")

        # ---------------------------------------------------------
        # ProfileUpdate
        # ---------------------------------------------------------

        update_schema = ProfileUpdate(
            full_name="Shafin Thiyam",
            title="Senior Associate Consultant",
            email="shafin@example.com",
            phone="+91-9876543210",
            location="Bengaluru",
            linkedin_url="https://linkedin.com/in/shafin",
            github_url="https://github.com/Shafin-Thiyam",
            portfolio_url="https://portfolio.example.com",
            summary="Senior Python Backend Developer",
            profile_image=None,
            resume_url=None,
        )

        print("✓ ProfileUpdate")

        # ---------------------------------------------------------
        # ORM -> Response
        # ---------------------------------------------------------

        profile = Profile(
            id=1,
            full_name="Shafin Thiyam",
            title="Associate Consultant",
            email="shafin@example.com",
            phone="+91-9876543210",
            location="Hyderabad",
            linkedin_url="https://linkedin.com/in/shafin",
            github_url="https://github.com/Shafin-Thiyam",
            portfolio_url="https://portfolio.example.com",
            summary="Python Backend Developer",
            profile_image=None,
            resume_url=None,
        )

        profile.created_at = datetime.now(UTC)
        profile.updated_at = datetime.now(UTC)

        response = ProfileResponse.model_validate(profile)

        assert response.id == 1
        assert response.email == "shafin@example.com"
        assert create_schema.email == "shafin@example.com"
        assert update_schema.title == "Senior Associate Consultant"
        assert response.full_name == "Shafin Thiyam"

        print("✓ ProfileResponse")

        print()
        print("=" * 60)
        print("All schema verification tests passed.")
        print("=" * 60)

    except Exception as exc:
        print()
        print("❌ Schema verification failed")
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()