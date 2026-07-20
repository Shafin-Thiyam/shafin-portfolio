"""
Verify EducationRepository structure.
"""

import sys

from app.db.session import SessionLocal
from app.models import Education
from app.repositories import EducationRepository


def main() -> None:
    """
    Verify EducationRepository.
    """

    print("=" * 60)
    print("Education Repository Verification")
    print("=" * 60)

    db = SessionLocal()

    try:

        # ---------------------------------------------------------
        # Repository Import / Initialization
        # ---------------------------------------------------------

        repository = EducationRepository(db)

        print("✓ Repository created")

        # ---------------------------------------------------------
        # Verify Model Binding
        # ---------------------------------------------------------

        assert repository.model is Education

        print("✓ Model binding verified")

        # ---------------------------------------------------------
        # Verify Database Session
        # ---------------------------------------------------------

        assert repository.db is db

        print("✓ Database session verified")

        # ---------------------------------------------------------
        # Verify CRUD Methods
        # ---------------------------------------------------------

        assert callable(repository.create)
        assert callable(repository.update)
        assert callable(repository.delete)
        assert callable(repository.get_by_id)
        assert callable(repository.get_all)

        print("✓ CRUD methods verified")

        # ---------------------------------------------------------
        # Verify Custom Query Methods
        # ---------------------------------------------------------

        assert callable(repository.get_by_institution)
        assert callable(repository.get_by_degree)
        assert callable(repository.get_by_field_of_study)

        print("✓ Custom query methods verified")

        print()
        print("=" * 60)
        print("Repository Verification Summary")
        print("=" * 60)

        print("✓ Repository import")
        print("✓ Repository initialization")
        print("✓ Model binding")
        print("✓ Database session")
        print("✓ CRUD methods")
        print("✓ Custom query methods")

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

        db.close()

    print("=" * 60)
    print("Repository verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()