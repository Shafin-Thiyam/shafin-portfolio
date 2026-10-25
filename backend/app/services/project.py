
from sqlalchemy.orm import Session

from app.models import Project
from app.repositories import (
    ExperienceRepository,
    ProjectRepository,
)
from app.schemas import ProjectCreate, ProjectUpdate


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
        project_data: ProjectCreate,
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

        project = Project(**project_data.model_dump())

        return self.repository.create(project)

    def update(
        self,
        project_id: int,
        project_data: ProjectUpdate,
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

        updated_fields = project_data.model_dump()
        #updated_fields = project_data.model_dump(exclude_unset=True)

        for field, value in updated_fields.items():
            setattr(existing_project, field, value)

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