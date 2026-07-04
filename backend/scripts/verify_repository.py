"""
Repository infrastructure verification.

This script verifies the BaseRepository
without requiring application models.
"""

from sqlalchemy.orm import Session

from app.repositories import BaseRepository


def print_header() -> None:
    """Print script header."""

    print("\n" + "=" * 60)
    print("Repository Verification")
    print("=" * 60)


def print_footer() -> None:
    """Print script footer."""

    print("=" * 60)
    print("Repository verification completed successfully.")
    print("=" * 60 + "\n")


def verify_import() -> None:
    """
    Verify repository import.
    """

    print("\n[1] Import")

    print("✓ BaseRepository imported")


def verify_methods() -> None:
    """
    Verify CRUD methods.
    """

    print("\n[2] CRUD Methods")

    methods = (
        "create",
        "get_by_id",
        "get_all",
        "update",
        "delete",
        "exists",
        "count",
    )

    for method in methods:
        if hasattr(BaseRepository, method):
            print(f"✓ {method}()")
        else:
            raise RuntimeError(f"Missing method: {method}")


def verify_constructor() -> None:
    """
    Verify constructor signature.
    """

    print("\n[3] Constructor")

    annotations = BaseRepository.__init__.__annotations__

    expected = ("db", "model", "return")

    for item in expected:
        if item not in annotations:
            raise RuntimeError(f"Missing annotation: {item}")

    print("✓ Constructor verified")


def main() -> None:
    """
    Run repository verification.
    """

    print_header()

    verify_import()

    verify_methods()

    verify_constructor()

    print_footer()


if __name__ == "__main__":
    main()