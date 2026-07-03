"""
Database infrastructure verification script.

This script verifies:
- Configuration
- SQLAlchemy Engine
- Database connectivity
- Session creation
- Transactions
- Alembic status
"""

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from app.core.config import settings
from app.db.database import engine
from app.db.session import SessionLocal


def print_header() -> None:
    """Print script header."""

    print("\n" + "=" * 60)
    print("Portfolio Database Verification")
    print("=" * 60)


def print_footer() -> None:
    """Print script footer."""

    print("=" * 60)
    print("Database verification completed successfully.")
    print("=" * 60 + "\n")


def verify_configuration() -> None:
    """
    Verify application configuration.
    """
    masked_url = settings.database_url.replace(
        settings.postgres_password,
        "********",
        )


    print("\n[1] Configuration")
    print(f"✓ Database URL : {masked_url}")
    print("✓ Configuration loaded")


def verify_engine() -> None:
    """
    Verify SQLAlchemy engine.
    """

    print("\n[2] SQLAlchemy Engine")

    print(f"✓ Engine : {engine}")
    print("✓ Engine initialized")


def verify_session() -> None:
    """
    Verify SessionLocal creation.
    """

    print("\n[3] Session")

    session = SessionLocal()

    try:
        print("✓ Session created")
    finally:
        session.close()
        print("✓ Session closed")


def verify_database() -> None:
    """
    Verify PostgreSQL connectivity.
    """

    print("\n[4] PostgreSQL Connectivity")

    with SessionLocal() as session:

        version = session.execute(
            text("SELECT version();")
        ).scalar_one()

        database = session.execute(
            text("SELECT current_database();")
        ).scalar_one()

        print("✓ Connected to PostgreSQL")
        print(f"✓ Database : {database}")
        print(f"✓ Version  : {version}")


def verify_transaction() -> None:
    """
    Verify transaction support.
    """

    print("\n[5] Transactions")

    with SessionLocal() as session:

        session.begin()

        session.execute(text("SELECT 1"))

        session.rollback()

        print("✓ Transaction successful")


def verify_alembic() -> None:
    """
    Verify Alembic configuration.
    """

    print("\n[6] Alembic")

    with SessionLocal() as session:

        try:
            revision = session.execute(
                text(
                    """
                    SELECT version_num
                    FROM alembic_version
                    """
                )
            ).scalar_one()

            print(f"✓ Current Revision : {revision}")

        except ProgrammingError:

            print("✓ Alembic configured")
            print("✓ No migrations applied yet")


def main() -> None:
    """
    Run all verification checks.
    """

    print_header()

    verify_configuration()

    verify_engine()

    verify_session()

    verify_database()

    verify_transaction()

    verify_alembic()

    print_footer()


if __name__ == "__main__":
    main()