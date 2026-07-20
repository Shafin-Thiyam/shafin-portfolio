"""
Verify Education model.
"""

import sys
from datetime import date

from app.models import Education


def main() ->None:
    """
    Verify Education model.
    """

    print("=" * 60)
    print("Education Model Verification")
    print("=" * 60)

    try:

        # ---------------------------------------------------------
        # Create model instance
        # ---------------------------------------------------------

        education = Education(
            institution="Anna University",
            degree="Bachelor of Engineering",
            field_of_study="Computer Science",
            start_date=date(2018, 8, 1),
            end_date=date(2022, 5, 31),
            grade="8.9 CGPA",
            description="Graduated with distinction.",
            display_order=1,
        )

        print("✓ Education instance created")

        # ---------------------------------------------------------
        # Verify table name
        # ---------------------------------------------------------

        assert Education.__tablename__ == "educations"

        print("✓ Table name")

        # ---------------------------------------------------------
        # Verify fields
        # ---------------------------------------------------------

        assert education.institution == "Anna University"
        assert education.degree == "Bachelor of Engineering"
        assert education.field_of_study == "Computer Science"

        assert education.start_date == date(2018, 8, 1)
        assert education.end_date == date(2022, 5, 31)

        assert education.grade == "8.9 CGPA"

        assert (
            education.description
            == "Graduated with distinction."
        )

        assert education.display_order == 1

        print("✓ Model fields")

        # ---------------------------------------------------------
        # Verify inherited fields
        # ---------------------------------------------------------

        assert hasattr(education, "id")
        assert hasattr(education, "created_at")
        assert hasattr(education, "updated_at")

        print("✓ BaseModel inheritance")

        # ---------------------------------------------------------
        # Verify nullable fields
        # ---------------------------------------------------------

        ongoing = Education(
            institution="ABC University",
            degree="Master of Technology",
            field_of_study="Artificial Intelligence",
            start_date=date(2024, 8, 1),
            end_date=None,
            grade=None,
            description=None,
            display_order=2,
        )

        assert ongoing.end_date is None
        assert ongoing.grade is None
        assert ongoing.description is None

        print("✓ Nullable fields")

        print()
        print("=" * 60)
        print("Education Model Verification Summary")
        print("=" * 60)

        print("✓ Model creation")
        print("✓ Table name")
        print("✓ Field mapping")
        print("✓ BaseModel inheritance")
        print("✓ Nullable fields")

        print()
        print("🎉 Education model verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ Model verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    print("=" * 60)
    print("Model verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()