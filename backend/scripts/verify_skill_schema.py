"""
Verify Skill schemas.
"""

import sys
from datetime import datetime, UTC

from pydantic import ValidationError

from app.models import Skill
from app.schemas import (
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    SkillListResponse,
)


def main() -> None:
    """
    Verify Skill schemas.
    """

    print("=" * 60)
    print("Skill Schema Verification")
    print("=" * 60)

    try:

        # ---------------------------------------------------------
        # SkillCreate
        # ---------------------------------------------------------

        create = SkillCreate(
            name="Python",
            category="Backend",
            proficiency=95,
            display_order=1,
        )

        assert create.name == "Python"

        print("✓ SkillCreate")

        # ---------------------------------------------------------
        # SkillUpdate
        # ---------------------------------------------------------

        update = SkillUpdate(
            name="FastAPI",
            category="Backend",
            proficiency=98,
            display_order=2,
        )

        assert update.name == "FastAPI"

        print("✓ SkillUpdate")

        # ---------------------------------------------------------
        # ORM -> SkillResponse
        # ---------------------------------------------------------

        model = Skill(
            id=1,
            name="Python",
            category="Backend",
            proficiency=95,
            display_order=1,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        response = SkillResponse.model_validate(model)
        
        assert response.id == 1
        assert response.name == "Python"
        assert response.category == "Backend"
        assert response.proficiency == 95
        assert response.display_order == 1
        assert response.created_at is not None
        assert response.updated_at is not None
        
        print("✓ SkillResponse from ORM")

        payload = response.model_dump()

        assert payload["name"] == "Python"
        assert payload["category"] == "Backend"

        print("✓ Serialization")


        # ---------------------------------------------------------
        # ApiResponse
        # ---------------------------------------------------------

        api_response = SkillListResponse(
            success=True,
            message="Skills retrieved successfully.",
            data=[response],
        )

        assert api_response.success is True
        assert api_response.message == "Skills retrieved successfully."
        assert len(api_response.data) == 1

        print("✓ SkillListResponse")

        # ---------------------------------------------------------
        # Boundary validation
        # ---------------------------------------------------------

        SkillCreate(
            name="Docker",
            category="DevOps",
            proficiency=0,
            display_order=0,
        )

        SkillCreate(
            name="Kubernetes",
            category="DevOps",
            proficiency=100,
            display_order=999,
        )

        print("✓ Boundary validation")

        # ---------------------------------------------------------
        # Invalid value validation
        # ---------------------------------------------------------

        try:
            SkillCreate(
                name="",
                category="Backend",
                proficiency=200,
                display_order=-1,
            )

            raise AssertionError("Expected ValidationError")

        except ValidationError:
            print("✓ Validation")

        # ---------------------------------------------------------
        # Extra field validation
        # ---------------------------------------------------------

        try:
            SkillCreate(
                name="Python",
                category="Backend",
                proficiency=95,
                display_order=1,
                invalid="test",
            )

            raise AssertionError("Expected ValidationError")

        except ValidationError:
            print("✓ Extra field validation")
        
        
    except AssertionError as exc:

        print()
        print("❌ Schema verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    print("=" * 60)
    print("Schema verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()