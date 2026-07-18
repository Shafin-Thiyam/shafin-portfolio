"""
Verify Skill schemas.
"""

import sys
from datetime import datetime

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
        )

        response = SkillResponse.model_validate(model)

        assert response.id == 1
        assert response.name == "Python"

        print("✓ SkillResponse from ORM")

        # ---------------------------------------------------------
        # ApiResponse
        # ---------------------------------------------------------

        api_response = SkillListResponse(
            success=True,
            message="Skills retrieved successfully.",
            data=[response],
        )

        assert api_response.success is True
        assert len(api_response.data) == 1

        print("✓ SkillListResponse")

        # ---------------------------------------------------------
        # Validation
        # ---------------------------------------------------------

        try:

            SkillCreate(
                name="",
                category="Backend",
                proficiency=200,
                display_order=-1,
            )

            raise AssertionError(
                "Validation should fail."
            )

        except ValidationError:

            print("✓ Validation")

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