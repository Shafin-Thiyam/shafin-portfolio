"""
Model metadata verification.

Verifies SQLAlchemy model registration before creating migrations.
"""

from app.db import Base
from app.models import (
    Profile,
    Skill,
    Education,
    Experience,
    experience_skills,
)


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


def verify_experience_registration() -> None:
    """
    Verify Experience model registration.
    """

    print("\n[3] Experience Model")

    print(f"✓ Model: {Experience.__name__}")
    print(f"✓ Table: {Experience.__tablename__}")


def verify_metadata() -> None:
    """
    Verify SQLAlchemy metadata.
    """

    print("\n[4] SQLAlchemy Metadata")

    tables = Base.metadata.tables

    expected_tables = (
        "profiles",
        "skills",
        "experiences",
        "experience_skills",
    )

    for table in expected_tables:

        if table not in tables:
            raise RuntimeError(
                f"{table} table not registered"
            )

        print(f"✓ {table} table registered")


def verify_profile_columns() -> None:
    """
    Verify Profile model columns.
    """

    print("\n[5] Profile Columns")

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
            raise RuntimeError(
                f"Missing Profile column: {column}"
            )

        print(f"✓ {column}")


def verify_skill_columns() -> None:
    """
    Verify Skill model columns.
    """

    print("\n[6] Skill Columns")

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
            raise RuntimeError(
                f"Missing Skill column: {column}"
            )

        print(f"✓ {column}")


def verify_experience_columns() -> None:
    """
    Verify Experience model columns.
    """

    print("\n[7] Experience Columns")

    table = Base.metadata.tables["experiences"]

    expected_columns = (
        "id",
        "company",
        "designation",
        "employment_type",
        "location",
        "location_type",
        "start_date",
        "end_date",
        "is_current",
        "description",
        "display_order",
        "created_at",
        "updated_at",
    )

    for column in expected_columns:

        if column not in table.columns:
            raise RuntimeError(
                f"Missing Experience column: {column}"
            )

        print(f"✓ {column}")


def verify_experience_skill_columns() -> None:
    """
    Verify Experience-Skill association table columns.
    """

    print("\n[8] Experience-Skill Association")

    table = Base.metadata.tables["experience_skills"]

    expected_columns = (
        "experience_id",
        "skill_id",
    )

    for column in expected_columns:

        if column not in table.columns:
            raise RuntimeError(
                f"Missing experience_skills column: {column}"
            )

        print(f"✓ {column}")


def main() -> None:
    """
    Execute model verification.
    """

    print_header()

    verify_profile_registration()
    verify_skill_registration()
    #verify_experience_registration()

    verify_metadata()

    verify_profile_columns()
    verify_skill_columns()
    verify_experience_columns()
    verify_experience_skill_columns()

    print_footer()


if __name__ == "__main__":
    main()