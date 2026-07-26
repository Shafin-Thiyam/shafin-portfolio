"""
Verify EducationRepository behaviour.
"""

from datetime import date
import sys

from app.db.session import SessionLocal
from app.repositories import EducationRepository
from app.schemas import EducationCreate


TEST_INSTITUTION = "Repository Test University"
TEST_DEGREE = "Bachelor of Engineering"
TEST_FIELD = "Computer Science"


def cleanup(repository: EducationRepository) -> None:
    """
    Remove repository test records.
    """

    education = repository.get_by_institution_and_degree(
        TEST_INSTITUTION,
        TEST_DEGREE,
    )

    if education is not None:
        repository.delete(education)

    education = repository.get_by_institution_and_degree(
        TEST_INSTITUTION,
        "Master of Technology",
    )

    if education is not None:
        repository.delete(education)


def main() -> None:
    """
    Verify EducationRepository.
    """

    print("=" * 60)
    print("Education Repository Verification")
    print("=" * 60)

    db = SessionLocal()

    try:

        repository = EducationRepository(db)

        cleanup(repository)

        print("✓ Repository created")

        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        education = repository.create(
            EducationCreate(
                institution=TEST_INSTITUTION,
                degree=TEST_DEGREE,
                field_of_study=TEST_FIELD,
                start_date=date(2015, 8, 1),
                end_date=date(2019, 5, 31),
                grade="8.9 CGPA",
                description="Repository verification record.",
                display_order=999,
            )
        )

        assert education.id is not None

        print("✓ Create verified")

        # ---------------------------------------------------------
        # Get by ID
        # ---------------------------------------------------------

        fetched = repository.get_by_id(education.id)

        assert fetched is not None
        assert fetched.institution == TEST_INSTITUTION

        print("✓ Get by ID verified")

        # ---------------------------------------------------------
        # Get All
        # ---------------------------------------------------------

        educations = repository.get_all()

        assert any(
            e.id == education.id
            for e in educations
        )

        print("✓ Get all verified")

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        education.degree = "Master of Technology"

        repository.update(education)

        updated = repository.get_by_id(education.id)

        assert updated is not None
        assert updated.degree == "Master of Technology"

        print("✓ Update verified")

        # ---------------------------------------------------------
        # Institution Query
        # ---------------------------------------------------------

        by_institution = repository.get_by_institution(
            TEST_INSTITUTION
        )

        assert by_institution is not None

        print("✓ Institution query verified")

        # ---------------------------------------------------------
        # Degree Query
        # ---------------------------------------------------------

        by_degree = repository.get_by_degree(
            "Master of Technology"
        )

        assert any(
            e.id == education.id
            for e in by_degree
        )

        print("✓ Degree query verified")

        # ---------------------------------------------------------
        # Institution + Degree Query
        # ---------------------------------------------------------

        by_pair = repository.get_by_institution_and_degree(
            TEST_INSTITUTION,
            "Master of Technology",
        )

        assert by_pair is not None
        assert by_pair.id == education.id

        print("✓ Institution + degree query verified")

        # ---------------------------------------------------------
        # Field of Study Query
        # ---------------------------------------------------------

        by_field = repository.get_by_field_of_study(
            TEST_FIELD
        )

        assert any(
            e.id == education.id
            for e in by_field
        )

        print("✓ Field of study query verified")

        # ---------------------------------------------------------
        # Delete
        # ---------------------------------------------------------

        repository.delete(education)

        deleted = repository.get_by_id(
            education.id
        )

        assert deleted is None

        print("✓ Delete verified")

        print()
        print("=" * 60)
        print("Repository Verification Summary")
        print("=" * 60)

        print("✓ CRUD operations")
        print("✓ Custom queries")
        print("✓ Repository behaviour")

        print()
        print("🎉 EducationRepository verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ Repository verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    finally:

        cleanup(repository)
        db.close()

    print("=" * 60)
    print("Repository verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()