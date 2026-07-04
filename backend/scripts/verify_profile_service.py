"""
Verify ProfileService functionality.
"""

import sys

from app.db.session import SessionLocal
from app.models import Profile
from app.services import ProfileService


def main() -> None:
    """
    Verify ProfileService.
    """

    print("=" * 60)
    print("Profile Service Verification")
    print("=" * 60)

    db = SessionLocal()

    try:
        service = ProfileService(db)

        print("✓ Service created successfully")

    except Exception as exc:
        print()
        print("❌ Service initialization failed")
        print(exc)
        sys.exit(1)

    finally:
        db.close()

    print("=" * 60)
    print("Verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()