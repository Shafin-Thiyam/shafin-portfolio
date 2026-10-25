
import sys
from datetime import date

from app.db.session import SessionLocal
from app.models import Experience, Project
from app.repositories import ExperienceRepository
from app.schemas import (
    ExperienceCreate,
    ProjectCreate,
    ProjectUpdate,
)
from app.services.project import ProjectService




INVALID_PROJECT_ID = -999999
INVALID_EXPERIENCE_ID = -999999


def assert_equal(actual, expected, message: str) -> None:
    """Assert that two values are equal."""

    if actual != expected:
        raise AssertionError(
            f"{message} Expected {expected!r}, got {actual!r}."
        )


def assert_true(condition: bool, message: str) -> None:
    """Assert that a condition is true."""

    if not condition:
        raise AssertionError(message)


def assert_raises(
    exception_type: type[Exception],
    operation,
    message: str,
) -> None:
    """Assert that an operation raises the expected exception."""

    try:
        operation()
    except exception_type:
        return
    except Exception as exc:
        raise AssertionError(
            f"{message} Expected {exception_type.__name__}, "
            f"got {type(exc).__name__}: {exc}"
        ) from exc

    raise AssertionError(
        f"{message} Expected {exception_type.__name__}, "
        "but no exception was raised."
    )


def main() -> None:
    """Verify ProjectService behaviour against the database."""

    print("=" * 60)
    print("Project Service Verification")
    print("=" * 60)

    db = SessionLocal()

    experience_ids: list[int] = []
    project_ids: list[int] = []

    try:
        # =====================================================
        # 1. Service initialization
        # =====================================================

        service = ProjectService(db)

        assert_true(
            service.repository is not None,
            "Project repository should be initialized.",
        )

        assert_true(
            service.experience_repository is not None,
            "Experience repository should be initialized.",
        )

        print("PASS: service initialization")

        # =====================================================
        # 2. Create test experiences
        # =====================================================

        experience_repository = ExperienceRepository(db)

        experience_1 = experience_repository.create(
            ExperienceCreate(
                company="Project Service Test Company A",
                designation="Python Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Hybrid",
                start_date=date(2022, 1, 1),
                end_date=date(2024, 1, 1),
                is_current=False,
                description="Project service verification.",
                display_order=980,
            )
        )

        experience_ids.append(experience_1.id)

        experience_2 = experience_repository.create(
            ExperienceCreate(
                company="Project Service Test Company B",
                designation="Backend Engineer",
                employment_type="Full-time",
                location="Bangalore",
                location_type="Remote",
                start_date=date(2024, 1, 1),
                end_date=None,
                is_current=True,
                description="Project service verification.",
                display_order=981,
            )
        )

        experience_ids.append(experience_2.id)

        print("PASS: test experiences created")

        # =====================================================
        # 3. Project creation
        # =====================================================

        project_1 = service.create(
            ProjectCreate(
                experience_id=experience_1.id,
                title="Service Test Project A",
                description="First service verification project.",
                role="Backend Developer",
                technologies=["Python", "FastAPI"],
                project_url=None,
                repository_url=None,
                start_date=date(2023, 1, 1),
                end_date=date(2023, 6, 1),
                display_order=20,
            )
        )

        project_ids.append(project_1.id)

        assert_true(
            project_1.id is not None,
            "Created project should have an ID.",
        )

        assert_equal(
            project_1.title,
            "Service Test Project A",
            "Created project title mismatch.",
        )

        print("PASS: create()")

        project_2 = service.create(
            ProjectCreate(
                experience_id=experience_1.id,
                title="Service Test Project B",
                description="Second service verification project.",
                role="Python Developer",
                technologies=["Python", "SQLAlchemy"],
                project_url=None,
                repository_url=None,
                start_date=date(2023, 6, 1),
                end_date=date(2023, 12, 1),
                display_order=10,
            )
        )

        project_ids.append(project_2.id)

        project_3 = service.create(
            ProjectCreate(
                experience_id=experience_2.id,
                title="Service Test Project C",
                description="Third service verification project.",
                role="Software Engineer",
                technologies=["Python", "PostgreSQL"],
                project_url=None,
                repository_url=None,
                start_date=date(2024, 1, 1),
                end_date=None,
                display_order=5,
            )
        )

        project_ids.append(project_3.id)

        print("PASS: multiple projects created")

        # =====================================================
        # 4. Retrieval
        # =====================================================

        fetched = service.get_by_id(project_1.id)

        assert_true(
            fetched is not None,
            "Project should be retrievable by ID.",
        )

        assert_equal(
            fetched.id,
            project_1.id,
            "Retrieved project ID mismatch.",
        )

        assert_equal(
            service.get_by_id(INVALID_PROJECT_ID),
            None,
            "Missing project should return None.",
        )

        print("PASS: get_by_id()")

        all_projects = service.get_all()

        positions = [
            (project.display_order, project.id)
            for project in all_projects
        ]

        assert_equal(
            positions,
            sorted(positions),
            "All projects should be ordered by display order, then ID.",
        )

        print("PASS: get_all() ordering")

        experience_projects = service.get_by_experience_id(
            experience_1.id
        )

        assert_equal(
            {project.id for project in experience_projects},
            {project_1.id, project_2.id},
            "Experience project filtering mismatch.",
        )

        positions = [
            (project.display_order, project.id)
            for project in experience_projects
        ]

        assert_equal(
            positions,
            sorted(positions),
            "Experience projects should be ordered by display order, then ID.",
        )

        print("PASS: get_by_experience_id()")

        empty_projects = service.get_by_experience_id(
            experience_2.id
        )

        assert_equal(
            [project.id for project in empty_projects],
            [project_3.id],
            "Second experience should initially have its own project.",
        )

        # Remove the third project so the second experience has no projects.
        service.delete(project_3.id)
        project_ids.remove(project_3.id)

        empty_projects = service.get_by_experience_id(
            experience_2.id
        )

        assert_equal(
            empty_projects,
            [],
            "Experience with no projects should return an empty list.",
        )

        print("PASS: empty project list")

        # =====================================================
        # 5. Parent experience validation
        # =====================================================

        assert_raises(
            ValueError,
            lambda: service.get_by_experience_id(
                INVALID_EXPERIENCE_ID
            ),
            "Missing experience lookup should fail.",
        )

        assert_raises(
            ValueError,
            lambda: service.create(
                ProjectCreate(
                    experience_id=INVALID_EXPERIENCE_ID,
                    title="Invalid Parent Project",
                    description=None,
                    role=None,
                    technologies=[],
                    project_url=None,
                    repository_url=None,
                    start_date=None,
                    end_date=None,
                    display_order=999,
                )
            ),
            "Creating a project for a missing experience should fail.",
        )

        print("PASS: parent experience validation")

        # =====================================================
        # 6. Update
        # =====================================================

        project_update = ProjectUpdate(
            experience_id=experience_1.id,
            title="Updated Service Test Project A",
            description="Updated project description.",
            role="Senior Backend Developer",
            technologies=["Python", "FastAPI", "PostgreSQL"],
            project_url=None,
            repository_url=None,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 7, 1),
            display_order=30,
        )

        updated = service.update(
            project_1.id,
            project_update,
        )

        assert_equal(
            updated.title,
            "Updated Service Test Project A",
            "Updated title mismatch.",
        )

        assert_equal(
            updated.role,
            "Senior Backend Developer",
            "Updated role mismatch.",
        )

        assert_equal(
            updated.technologies,
            ["Python", "FastAPI", "PostgreSQL"],
            "Updated technologies mismatch.",
        )

        print("PASS: update()")

        assert_raises(
            ValueError,
            lambda: service.update(
                INVALID_PROJECT_ID,
                project_update,
            ),
            "Updating a missing project should fail.",
        )

        print("PASS: missing project update validation")

        invalid_parent_update = ProjectUpdate(
            experience_id=999999999,
            title="Invalid Parent Update",
            description=None,
            role=None,
            technologies=[],
            project_url=None,
            repository_url=None,
            start_date=None,
            end_date=None,
            display_order=999,
        )

        assert_raises(
            ValueError,
            lambda: service.update(
                project_1.id,
                invalid_parent_update,
            ),
            "Updating with a missing experience should fail.",
        )

        print("PASS: update parent validation")

        # =====================================================
        # 7. Delete
        # =====================================================

        service.delete(project_2.id)
        project_ids.remove(project_2.id)

        assert_equal(
            service.get_by_id(project_2.id),
            None,
            "Deleted project should no longer exist.",
        )

        print("PASS: delete()")

        assert_raises(
            ValueError,
            lambda: service.delete(INVALID_PROJECT_ID),
            "Deleting a missing project should fail.",
        )

        print("PASS: missing project delete validation")

        print()
        print("=" * 60)
        print("Project Service Verification Summary")
        print("=" * 60)
        print("All ProjectService checks passed.")
        print("=" * 60)

    finally:
        # =====================================================
        # 8. Cleanup
        # =====================================================

        try:
            for project_id in project_ids:
                project = db.get(Project, project_id)

                if project is not None:
                    db.delete(project)

            db.flush()

            for experience_id in experience_ids:
                experience = db.get(
                    Experience,
                    experience_id,
                )

                if experience is not None:
                    db.delete(experience)

            db.commit()
            print("Cleanup completed.")

        except Exception:
            db.rollback()
            print(
                "Cleanup failed. Inspect the database for "
                "remaining verification records.",
                file=sys.stderr,
            )
            raise

        finally:
            db.close()


if __name__ == "__main__":
    main()
