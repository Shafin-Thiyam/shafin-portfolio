"""
Verify EducationService functionality.
"""

import sys
from datetime import date

from app.db.session import SessionLocal
from app.schemas import (
    EducationCreate,
    EducationUpdate,
)
from app.services import EducationService


def main() -> None:
    """
    Verify EducationService.
    """

    print("=" * 60)
    print("Education Service Verification")
    print("=" * 60)

    db = SessionLocal()

    try:

        # ---------------------------------------------------------
        # Service Initialization
        # ---------------------------------------------------------

        service = EducationService(db)

        print("✓ Service created")

        # ---------------------------------------------------------
        # Clean Existing Data
        # ---------------------------------------------------------

        for education in service.get_all_educations():
            service.delete_education(education.id)

        print("✓ Existing educations cleaned")

        # ---------------------------------------------------------
        # Create Education
        # ---------------------------------------------------------

        education = service.create_education(
            EducationCreate(
                institution="Anna University",
                degree="Bachelor of Engineering",
                field_of_study="Computer Science",
                start_date=date(2010, 8, 1),
                end_date=date(2014, 5, 31),
                grade="8.5 CGPA",
                description="Graduated with distinction.",
                display_order=1,
            )
        )

        assert education.id is not None
        assert education.institution == "Anna University"
        assert education.degree == "Bachelor of Engineering"

        education_id = education.id

        print("✓ create_education()")

        # ---------------------------------------------------------
        # Verify Duplicate Institution
        # ---------------------------------------------------------

        try:

            service.create_education(
                EducationCreate(
                    institution="Anna University",
                    degree="Bachelor of Engineering",
                    field_of_study="Computer Science",
                    start_date=date(2010, 8, 1),
                    end_date=date(2014, 5, 31),
                    grade="8.5 CGPA",
                    description="Duplicate",
                    display_order=2,
                )
            )

            raise AssertionError(
                "Duplicate validation failed."
            )

        except ValueError:

            print("✓ Duplicate validation")

        # ---------------------------------------------------------
        # Verify get_all_educations()
        # ---------------------------------------------------------

        educations = service.get_all_educations()

        assert len(educations) == 1

        print("✓ get_all_educations()")

        # ---------------------------------------------------------
        # Verify get_education()
        # ---------------------------------------------------------

        retrieved = service.get_education(
            education_id
        )

        assert retrieved is not None
        assert retrieved.id == education_id

        print("✓ get_education()")

        # ---------------------------------------------------------
        # Verify get_education_by_institution()
        # ---------------------------------------------------------

        retrieved = service.get_education_by_institution(
            "Anna University"
        )

        assert retrieved is not None
        assert retrieved.id == education_id

        print("✓ get_education_by_institution()")

        # ---------------------------------------------------------
        # Verify get_educations_by_degree()
        # ---------------------------------------------------------

        educations = service.get_educations_by_degree(
            "Bachelor of Engineering"
        )

        assert len(educations) == 1

        print("✓ get_educations_by_degree()")

        # ---------------------------------------------------------
        # Verify get_educations_by_field_of_study()
        # ---------------------------------------------------------

        educations = (
            service.get_educations_by_field_of_study(
                "Computer Science"
            )
        )

        assert len(educations) == 1

        print("✓ get_educations_by_field_of_study()")

        # ---------------------------------------------------------
        # Verify update_education()
        # ---------------------------------------------------------

        updated = service.update_education(
            education_id,
            EducationUpdate(
                institution="JNTU Hyderabad",
                degree="Master of Technology",
                field_of_study="Software Engineering",
                start_date=date(2015, 8, 1),
                end_date=date(2017, 5, 31),
                grade="9.1 CGPA",
                description="Updated education",
                display_order=2,
            ),
        )

        assert updated.institution == "JNTU Hyderabad"
        assert updated.degree == "Master of Technology"
        assert updated.field_of_study == "Software Engineering"
        assert updated.display_order == 2

        print("✓ update_education()")

        # ---------------------------------------------------------
        # Verify Missing Update
        # ---------------------------------------------------------

        try:

            service.update_education(
                9999,
                EducationUpdate(
                    institution="Missing",
                    degree="Missing",
                    field_of_study="Missing",
                    start_date=date.today(),
                    end_date=None,
                    grade=None,
                    description=None,
                    display_order=0,
                ),
            )

            raise AssertionError(
                "Missing education validation failed."
            )

        except ValueError:

            print("✓ Missing education validation")

        # ---------------------------------------------------------
        # Verify Duplicate Update
        # ---------------------------------------------------------

        second = service.create_education(
            EducationCreate(
                institution="Osmania University",
                degree="Bachelor of Science",
                field_of_study="Mathematics",
                start_date=date(2008, 8, 1),
                end_date=date(2011, 5, 31),
                grade="8.0 CGPA",
                description=None,
                display_order=3,
            )
        )

        try:

            service.update_education(
                second.id,
                EducationUpdate(
                    institution="JNTU Hyderabad",
                    degree="Bachelor of Science",
                    field_of_study="Mathematics",
                    start_date=date(2008, 8, 1),
                    end_date=date(2011, 5, 31),
                    grade="8.0 CGPA",
                    description=None,
                    display_order=3,
                ),
            )

            raise AssertionError(
                "Duplicate update validation failed."
            )

        except ValueError:

            print("✓ Duplicate update validation")

        # ---------------------------------------------------------
        # Verify delete_education()
        # ---------------------------------------------------------

        service.delete_education(
            education_id
        )

        assert (
            service.get_education(
                education_id
            )
            is None
        )

        print("✓ delete_education()")

        # ---------------------------------------------------------
        # Verify Missing Delete
        # ---------------------------------------------------------

        try:

            service.delete_education(
                9999
            )

            raise AssertionError(
                "Missing delete validation failed."
            )

        except ValueError:

            print("✓ Missing delete validation")

        print()
        print("=" * 60)
        print("Service Verification Summary")
        print("=" * 60)

        print("✓ Create")
        print("✓ Read")
        print("✓ Update")
        print("✓ Delete")
        print("✓ Duplicate validation")
        print("✓ Missing record validation")
        print("✓ Custom queries")

        print()
        print("🎉 EducationService verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ Service verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    finally:

        db.close()

    print("=" * 60)
    print("Service verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()