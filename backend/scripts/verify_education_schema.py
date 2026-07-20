"""
Verify Education schemas.
"""

import sys
from datetime import UTC
from datetime import date
from datetime import datetime

from pydantic import ValidationError

from app.models import Education
from app.schemas import (
    EducationCreate,
    EducationListResponse,
    EducationResponse,
    EducationUpdate,
)


def main() -> None:
    """
    Verify Education schemas.
    """

    print("=" * 60)
    print("Education Schema Verification")
    print("=" * 60)

    try:

        # ---------------------------------------------------------
        # EducationCreate
        # ---------------------------------------------------------

        create = EducationCreate(
            institution="Anna University",
            degree="Bachelor of Engineering",
            field_of_study="Computer Science",
            start_date=date(2010, 8, 1),
            end_date=date(2014, 5, 31),
            grade="8.5 CGPA",
            description="Graduated with distinction.",
            display_order=1,
        )

        assert create.institution == "Anna University"

        print("✓ EducationCreate")

        # ---------------------------------------------------------
        # EducationUpdate
        # ---------------------------------------------------------

        update = EducationUpdate(
            institution="JNTU Hyderabad",
            degree="Master of Technology",
            field_of_study="Software Engineering",
            start_date=date(2015, 8, 1),
            end_date=date(2017, 5, 31),
            grade="9.1 CGPA",
            description="Postgraduate program.",
            display_order=2,
        )

        assert update.institution == "JNTU Hyderabad"

        print("✓ EducationUpdate")

        # ---------------------------------------------------------
        # ORM -> EducationResponse
        # ---------------------------------------------------------

        model = Education(
            id=1,
            institution="Anna University",
            degree="Bachelor of Engineering",
            field_of_study="Computer Science",
            start_date=date(2010, 8, 1),
            end_date=date(2014, 5, 31),
            grade="8.5 CGPA",
            description="Graduated with distinction.",
            display_order=1,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        response = EducationResponse.model_validate(model)

        assert response.id == 1
        assert response.institution == "Anna University"
        assert response.degree == "Bachelor of Engineering"
        assert response.field_of_study == "Computer Science"
        assert response.start_date == date(2010, 8, 1)
        assert response.end_date == date(2014, 5, 31)
        assert response.grade == "8.5 CGPA"
        assert response.description == "Graduated with distinction."
        assert response.display_order == 1
        assert response.created_at is not None
        assert response.updated_at is not None

        print("✓ EducationResponse from ORM")

        # ---------------------------------------------------------
        # Serialization
        # ---------------------------------------------------------

        payload = response.model_dump()

        assert payload["institution"] == "Anna University"
        assert payload["degree"] == "Bachelor of Engineering"
        assert payload["field_of_study"] == "Computer Science"
        assert payload["display_order"] == 1

        print("✓ Serialization")

        # ---------------------------------------------------------
        # ApiResponse
        # ---------------------------------------------------------

        api_response = EducationListResponse(
            success=True,
            message="Educations retrieved successfully.",
            data=[response],
        )

        assert api_response.success is True
        assert api_response.message == "Educations retrieved successfully."
        assert len(api_response.data) == 1

        print("✓ EducationListResponse")

        # ---------------------------------------------------------
        # Boundary validation
        # ---------------------------------------------------------

        EducationCreate(
            institution="A",
            degree="B",
            field_of_study="C",
            start_date=date(2020, 1, 1),
            end_date=None,
            grade=None,
            description=None,
            display_order=0,
        )

        print("✓ Boundary validation")

        # ---------------------------------------------------------
        # Invalid value validation
        # ---------------------------------------------------------

        try:

            EducationCreate(
                institution="",
                degree="",
                field_of_study="",
                start_date=date(2020, 1, 1),
                end_date=None,
                grade=None,
                description=None,
                display_order=-1,
            )

            raise AssertionError("Expected ValidationError")

        except ValidationError:

            print("✓ Validation")

        # ---------------------------------------------------------
        # Extra field validation
        # ---------------------------------------------------------

        try:

            EducationCreate(
                institution="Anna University",
                degree="Bachelor of Engineering",
                field_of_study="Computer Science",
                start_date=date(2010, 8, 1),
                end_date=date(2014, 5, 31),
                grade="8.5 CGPA",
                description="Graduated with distinction.",
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
    print("Education Schema Verification Summary")
    print("=" * 60)

    print("✓ EducationCreate")
    print("✓ EducationUpdate")
    print("✓ ORM serialization")
    print("✓ Response serialization")
    print("✓ EducationListResponse")
    print("✓ Boundary validation")
    print("✓ Validation")
    print("✓ Extra field validation")

    print()
    print("🎉 All Education schema verification tests passed successfully.")
    print("=" * 60)
    print("Schema verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()