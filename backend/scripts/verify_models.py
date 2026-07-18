"""
Model metadata verification.

Verifies SQLAlchemy model registration before creating migrations.
"""

from app.db import Base
#from app.models.profile import Profile, Skill
from app.models import Profile, Skill

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


def verify_profile_registration() -> None:
    """
    Verify Profile model registration.
    """

    print("\n[1] Profile Model")

    print(f"✓ Model: {Profile.__name__}")

    print(f"✓ Table: {Profile.__tablename__}")

def verify_skill_registration() -> None:
    """
    Verify Skill model registration.
    """

    print("\n[2] Skill Model")

    print(f"✓ Model: {Skill.__name__}")
    print(f"✓ Table: {Skill.__tablename__}")

def verify_metadata() -> None:
    """
    Verify SQLAlchemy metadata.
    """

    print("\n[2] SQLAlchemy Metadata")

    tables = Base.metadata.tables
    
    expected_tables = (
        "profiles",
        "skills",
    )
    
    for table in expected_tables:
        if table not in tables:
            raise RuntimeError(f"{table} table not registered")
        
        print(f"✓ {table} table registered")


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

def verify_profile_columns() -> None:
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

def verify_skill_columns() -> None:
    """
    Verify Skill model columns.
    """

    print("\n[5] Skill Columns")

    table = Base.metadata.tables["skills"]

    expected_columns = (
        "id",
        "name",
        "category",
        "proficiency",
        "display_order",
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

    verify_profile_registration()
    verify_skill_registration()

    verify_metadata()

    verify_profile_columns()
    verify_skill_columns()

    print_footer()


if __name__ == "__main__":
    main()