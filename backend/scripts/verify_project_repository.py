"""
Verify ProjectRepository operations.

Covers:
- Model import
- Repository initialization and model binding
- Project creation and retrieval
- Ordered project retrieval
- Filtering by experience
- Empty query results
- Count and existence checks
- Update persistence
- Delete behavior
- Cleanup
"""

import sys
from datetime import date

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Experience, Project
from app.repositories import ExperienceRepository, ProjectRepository
from app.schemas import ExperienceCreate


def main() -> None:
    """Verify ProjectRepository behaviour."""

    print("=" * 60)
    print("Project Repository Verification")
    print("=" * 60)

    db = SessionLocal()

    experience_repository = None
    project_repository = None

    experience_ids: list[int] = []
    project_ids: list[int] = []

    try:
        # =========================================================
        # 1. Model and Repository Imports
        # =========================================================

        assert Project.__tablename__ == "projects"

        print("✓ Project model imports")

        assert ProjectRepository is not None

        print("✓ ProjectRepository imports")

        # =========================================================
        # 2. Repository Initialization
        # =========================================================

        experience_repository = ExperienceRepository(db)
        project_repository = ProjectRepository(db)

        assert project_repository.db is db
        assert project_repository.model is Project

        print("✓ Repository initialization and model binding")

        # =========================================================
        # 3. Create Test Experiences
        # =========================================================

        print()
        print("--- Test Data Setup ---")

        experience_1 = experience_repository.create(
            ExperienceCreate(
                company="Project Repository Test Company A",
                designation="Python Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Hybrid",
                start_date=date(2022, 1, 1),
                end_date=date(2024, 1, 1),
                is_current=False,
                description="Project repository verification.",
                display_order=990,
            )
        )

        experience_ids.append(experience_1.id)

        experience_2 = experience_repository.create(
            ExperienceCreate(
                company="Project Repository Test Company B",
                designation="Backend Engineer",
                employment_type="Full-time",
                location="Bangalore",
                location_type="Remote",
                start_date=date(2024, 1, 1),
                end_date=None,
                is_current=True,
                description="Project repository verification.",
                display_order=991,
            )
        )

        experience_ids.append(experience_2.id)

        assert experience_1.id is not None
        assert experience_2.id is not None

        print("✓ Test experiences created")

        # =========================================================
        # 4. Create Projects
        # =========================================================

        print()
        print("--- Project CRUD ---")

        project_1 = Project(
            experience_id=experience_1.id,
            title="Repository Test Project A",
            description="First project verification record.",
            role="Backend Developer",
            technologies=["Python", "FastAPI"],
            project_url=None,
            repository_url=None,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 6, 1),
            display_order=20,
        )

        project_1 = project_repository.create(project_1)
        project_ids.append(project_1.id)

        assert project_1.id is not None
        assert project_1.title == "Repository Test Project A"

        print("✓ create() persists a project and generates an ID")

        project_2 = Project(
            experience_id=experience_1.id,
            title="Repository Test Project B",
            description="Second project verification record.",
            role="Python Developer",
            technologies=["Python", "SQLAlchemy"],
            project_url=None,
            repository_url=None,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 12, 1),
            display_order=10,
        )

        project_2 = project_repository.create(project_2)
        project_ids.append(project_2.id)

        project_3 = Project(
            experience_id=experience_2.id,
            title="Repository Test Project C",
            description="Third project verification record.",
            role="Software Engineer",
            technologies=["Python", "PostgreSQL"],
            project_url=None,
            repository_url=None,
            start_date=date(2024, 1, 1),
            end_date=None,
            display_order=5,
        )

        project_3 = project_repository.create(project_3)
        project_ids.append(project_3.id)

        print("✓ Multiple projects created")

        # =========================================================
        # 5. Get by ID
        # =========================================================

        fetched = project_repository.get_by_id(project_1.id)

        assert fetched is not None
        assert fetched.id == project_1.id
        assert fetched.title == "Repository Test Project A"

        print("✓ get_by_id() works")

        # =========================================================
        # 6. get_all() Ordering
        # =========================================================

        all_projects = project_repository.get_all()

        expected_order = sorted(
            all_projects,
            key=lambda item: (item.display_order, item.id),
        )

        assert [
            item.id for item in all_projects
        ] == [
            item.id for item in expected_order
        ]

        print("✓ get_all() orders by display_order, then ID")

        # =========================================================
        # 7. Filter by Experience
        # =========================================================

        experience_1_projects = (
            project_repository.get_by_experience_id(
                experience_1.id
            )
        )

        assert len(experience_1_projects) == 2

        assert all(
            item.experience_id == experience_1.id
            for item in experience_1_projects
        )

        assert [
            item.display_order
            for item in experience_1_projects
        ] == [10, 20]

        assert [
            item.id for item in experience_1_projects
        ] == [
            project_2.id,
            project_1.id,
        ]

        print("✓ get_by_experience_id() filters and orders correctly")

        # =========================================================
        # 8. Empty Results
        # =========================================================

        empty_results = project_repository.get_by_experience_id(
            -999999
        )

        assert empty_results == []

        print("✓ Nonmatching experience ID returns an empty list")

        # =========================================================
        # 9. Count and Existence
        # =========================================================

        for project_id in project_ids:
            assert project_repository.exists(project_id)

        assert not project_repository.exists(-999999)

        print("✓ exists() works")

        for experience_id in experience_ids:
            expected_count = len(
                project_repository.get_by_experience_id(
                    experience_id
                )
            )

            assert expected_count == (
                2 if experience_id == experience_1.id else 1
            )

        initial_count = project_repository.count()

        assert initial_count >= len(project_ids)

        print("✓ count() works")

        # =========================================================
        # 10. Update and Persistence
        # =========================================================

        fetched = project_repository.get_by_id(project_1.id)

        assert fetched is not None

        fetched.title = "Updated Repository Test Project"
        fetched.description = "Updated verification description."
        fetched.technologies = ["Python", "FastAPI", "PostgreSQL"]

        updated = project_repository.update(fetched)

        assert updated.title == "Updated Repository Test Project"
        assert updated.description == "Updated verification description."

        # Expire cached ORM state and query again.
        db.expire_all()

        persisted = project_repository.get_by_id(project_1.id)

        assert persisted is not None
        assert persisted.title == "Updated Repository Test Project"
        assert persisted.description == "Updated verification description."
        assert persisted.technologies == [
            "Python",
            "FastAPI",
            "PostgreSQL",
        ]

        print("✓ update() persists changes")

        # =========================================================
        # 11. Delete
        # =========================================================

        project_to_delete = project_repository.get_by_id(
            project_2.id
        )

        assert project_to_delete is not None

        project_repository.delete(project_to_delete)

        assert project_repository.get_by_id(project_2.id) is None
        assert not project_repository.exists(project_2.id)

        print("✓ delete() removes a project")

        # =========================================================
        # 12. Cleanup
        # =========================================================

        print()
        print("--- Cleanup ---")

        for project_id in project_ids:
            project = project_repository.get_by_id(project_id)

            if project is not None:
                project_repository.delete(project)

        for experience_id in experience_ids:
            experience = experience_repository.get_by_id(
                experience_id
            )

            if experience is not None:
                experience_repository.delete(experience)

        # Verify that test records are gone.
        for project_id in project_ids:
            assert project_repository.get_by_id(project_id) is None

        for experience_id in experience_ids:
            assert experience_repository.get_by_id(experience_id) is None

        print("✓ Test data cleaned up")

        # =========================================================
        # Summary
        # =========================================================

        print()
        print("=" * 60)
        print("Project Repository Verification Summary")
        print("=" * 60)
        print("✓ Repository initialization")
        print("✓ Project creation and retrieval")
        print("✓ Ordered project retrieval")
        print("✓ Experience filtering")
        print("✓ Empty results")
        print("✓ Count and existence")
        print("✓ Update persistence")
        print("✓ Delete")
        print("✓ Cleanup")
        print()
        print("🎉 ProjectRepository verified successfully.")

    except Exception as exc:
        db.rollback()

        print()
        print("❌ Project repository verification failed")
        print(f"{type(exc).__name__}: {exc}")

        sys.exit(1)

    finally:
        # Defensive cleanup if verification fails midway.
        try:
            db.rollback()

            if project_repository is not None:
                for project_id in project_ids:
                    project = project_repository.get_by_id(project_id)

                    if project is not None:
                        project_repository.delete(project)

            if experience_repository is not None:
                for experience_id in experience_ids:
                    experience = experience_repository.get_by_id(
                        experience_id
                    )

                    if experience is not None:
                        experience_repository.delete(experience)

        except Exception as cleanup_exc:
            db.rollback()
            print(f"⚠ Cleanup warning: {cleanup_exc}")

        finally:
            db.close()

        print("=" * 60)
        print("Repository verification finished.")
        print("=" * 60)


if __name__ == "__main__":
    main()