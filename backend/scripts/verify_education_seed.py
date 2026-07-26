"""
Verify seeded education data.
"""

import sys

from app.db.session import SessionLocal
from app.repositories import EducationRepository
from scripts.seed_education import main as seed_main


def main() -> None:
    """
    Verify education seed data.
    """

    print("=" * 60)
    print("Education Seed Verification")
    print("=" * 60)

    db = SessionLocal()

    try:

        repository = EducationRepository(db)

        # ---------------------------------------------------------
        # Database Connection
        # ---------------------------------------------------------

        assert db is not None

        print("✓ Database connected")

        # ---------------------------------------------------------
        # Education Records Exist
        # ---------------------------------------------------------

        educations = repository.get_all()

        assert len(educations) >= 2

        print("✓ Education records found")

        # ---------------------------------------------------------
        # MCA Education
        # ---------------------------------------------------------

        mca = repository.get_by_institution_and_degree(
            "Mumbai University",
            "M.C.A",
        )

        assert mca is not None

        print("✓ MCA education verified")

        # ---------------------------------------------------------
        # B.Sc.IT Education
        # ---------------------------------------------------------

        bsc = repository.get_by_institution_and_degree(
            "Mumbai University",
            "B.Sc.IT",
        )

        assert bsc is not None

        print("✓ B.Sc.IT education verified")

        # ---------------------------------------------------------
        # Display Order
        # ---------------------------------------------------------

        assert mca.display_order == 1
        assert bsc.display_order == 2

        print("✓ Display order verified")

        # ---------------------------------------------------------
        # Duplicate Prevention
        # ---------------------------------------------------------

        duplicate_mca = [
            education
            for education in educations
            if (
                education.institution == "Mumbai University"
                and education.degree == "M.C.A"
            )
        ]

        duplicate_bsc = [
            education
            for education in educations
            if (
                education.institution == "Mumbai University"
                and education.degree == "B.Sc.IT"
            )
        ]

        assert len(duplicate_mca) == 1
        assert len(duplicate_bsc) == 1

        print("✓ Duplicate prevention verified")

        # ---------------------------------------------------------
        # Required Fields
        # ---------------------------------------------------------

        for education in educations:

            assert education.institution
            assert education.degree
            assert education.field_of_study
            assert education.start_date
            assert education.display_order >= 0

        print("✓ Required fields verified")

        # ---------------------------------------------------------
        # Seed Idempotency
        # ---------------------------------------------------------

        count_before = len(repository.get_all())

        seed_main()

        count_after = len(repository.get_all())

        assert count_before == count_after

        print("✓ Seed idempotency verified")

        print()
        print("=" * 60)
        print("Education Seed Verification Summary")
        print("=" * 60)

        print("✓ Database connection")
        print("✓ Seed records")
        print("✓ Display order")
        print("✓ Duplicate prevention")
        print("✓ Required fields")
        print("✓ Idempotent seed")

        print()
        print("🎉 Education seed verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ Education seed verification failed")
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
    print("Seed verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()