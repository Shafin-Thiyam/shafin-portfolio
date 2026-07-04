"""
Model metadata verification.

Verifies SQLAlchemy model registration before creating migrations.
"""

from app.db import Base
from app.models.profile import Profile


def print_header() -> None:
    """Print script header."""

    print("\n" + "=" * 60)
    print("Model Metadata Verification")
    print("=" * 60)


def print_footer() -> None:
    """Print script footer."""

    print("=" * 60)
    print("Model verification completed successfully.")
    print("=" * 60 + "\n")


def verify_profile_model() -> None:
    """
    Verify Profile model registration.
    """

    print("\n[1] Profile Model")

    print(f"✓ Model: {Profile.__name__}")

    print(f"✓ Table: {Profile.__tablename__}")


def verify_metadata() -> None:
    """
    Verify SQLAlchemy metadata.
    """

    print("\n[2] SQLAlchemy Metadata")

    tables = Base.metadata.tables

    if "profiles" not in tables:
        raise RuntimeError("profiles table not registered")

    print("✓ profiles table registered")


def verify_columns() -> None:
    """
    Verify expected columns.
    """

    print("\n[3] Columns")

    table = Base.metadata.tables["profiles"]

    expected_columns = (
        "id",
        "full_name",
        "title",
        "email",
        "phone",
        "location",
        "linkedin_url",
        "github_url",
        "portfolio_url",
        "summary",
        "profile_image",
        "resume_url",
        "created_at",
        "updated_at",
    )

    for column in expected_columns:
        if column not in table.columns:
            raise RuntimeError(f"Missing column: {column}")

        print(f"✓ {column}")


def main() -> None:
    """
    Execute model verification.
    """

    print_header()

    verify_profile_model()

    verify_metadata()

    verify_columns()

    print_footer()


if __name__ == "__main__":
    main()