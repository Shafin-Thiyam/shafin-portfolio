
from sqlalchemy.orm import Session

from app.models import Project
from app.repositories import (
    ExperienceRepository,
    ProjectRepository,
)


PROJECT_NOT_FOUND_MESSAGE = "Project not found."
EXPERIENCE_NOT_FOUND_MESSAGE = "Experience not found."


class ProjectService:
    """
    Service layer for project operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize project service.
        """

        self.repository = ProjectRepository(db)
        self.experience_repository = ExperienceRepository(db)

    def get_all(self) -> list[Project]:
        """
        Retrieve all projects.
        """

        return self.repository.get_all()

    def get_by_id(
        self,
        project_id: int,
    ) -> Project | None:
        """
        Retrieve a project by ID.
        """

        return self.repository.get_by_id(project_id)

    def get_by_experience_id(
        self,
        experience_id: int,
    ) -> list[Project]:
        """
        Retrieve projects associated with an experience.

        Raises:
            ValueError: If the experience does not exist.
        """

        experience = self.experience_repository.get_by_id(
            experience_id
        )

        if experience is None:
            raise ValueError(EXPERIENCE_NOT_FOUND_MESSAGE)

        return self.repository.get_by_experience_id(
            experience_id
        )

    def create(
        self,
        project_data: Project,
    ) -> Project:
        """
        Create a project after validating its experience.

        Args:
            project_data: Validated project creation data.

        Raises:
            ValueError: If the referenced experience does not exist.
        """

        experience = self.experience_repository.get_by_id(
            project_data.experience_id
        )

        if experience is None:
            raise ValueError(EXPERIENCE_NOT_FOUND_MESSAGE)

        return self.repository.create(project_data)

    def update(
        self,
        project_id: int,
        project_data: Project,
    ) -> Project:
        """
        Update an existing project.

        Raises:
            ValueError: If the project or referenced experience
                does not exist.
        """

        existing_project = self.repository.get_by_id(
            project_id
        )

        if existing_project is None:
            raise ValueError(PROJECT_NOT_FOUND_MESSAGE)

        experience = self.experience_repository.get_by_id(
            project_data.experience_id
        )

        if experience is None:
            raise ValueError(EXPERIENCE_NOT_FOUND_MESSAGE)

        existing_project.experience_id = project_data.experience_id
        existing_project.title = project_data.title
        existing_project.description = project_data.description
        existing_project.role = project_data.role
        existing_project.technologies = project_data.technologies
        existing_project.project_url = project_data.project_url
        existing_project.repository_url = project_data.repository_url
        existing_project.start_date = project_data.start_date
        existing_project.end_date = project_data.end_date
        existing_project.display_order = project_data.display_order

        return self.repository.update(
            existing_project
        )

    def delete(
        self,
        project_id: int,
    ) -> None:
        """
        Delete an existing project.

        Raises:
            ValueError: If the project does not exist.
        """

        existing_project = self.repository.get_by_id(
            project_id
        )

        if existing_project is None:
            raise ValueError(PROJECT_NOT_FOUND_MESSAGE)

        self.repository.delete(existing_project)