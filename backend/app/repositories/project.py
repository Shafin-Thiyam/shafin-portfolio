from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project
from .base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Repository for Project model.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize the Project repository.
        """

        super().__init__(
            db,
            Project,
        )

    def get_all(self) -> list[Project]:
        """
        Retrieve all projects ordered by display order.

        Projects with the same display order are ordered by ID.
        """

        statement = (
            select(Project)
            .order_by(
                Project.display_order.asc(),
                Project.id.asc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_experience_id(
        self,
        experience_id: int,
    ) -> list[Project]:
        """
        Retrieve projects belonging to an experience.

        Results are ordered by display order, then ID.
        """

        statement = (
            select(Project)
            .where(
                Project.experience_id == experience_id,
            )
            .order_by(
                Project.display_order.asc(),
                Project.id.asc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )