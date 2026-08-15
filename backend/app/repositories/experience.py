"""
Experience repository.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Experience
from app.schemas import ExperienceCreate

from .base import BaseRepository


class ExperienceRepository(BaseRepository[Experience]):
    """
    Repository for Experience model.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize repository.
        """

        super().__init__(
            db,
            Experience,
        )

    def create(
        self,
        experience_data: ExperienceCreate,
    ) -> Experience:
        """
        Create a new experience.
        """

        experience = Experience(
            **experience_data.model_dump(),
        )

        return super().create(experience)

    def get_all(self) -> list[Experience]:
    
        """
        Retrieve all experiences ordered by display order.
        """

        statement = (
            select(Experience)
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_id(
        self,
        experience_id: int,
    ) -> Experience | None:
        """
        Retrieve an experience by ID.
        """

        return super().get_by_id(
            experience_id
        )

    def update(
        self,
        experience: Experience,
    ) -> Experience:
        """
        Update an existing experience.
        """

        return super().update(experience)

    def delete(
        self,
        experience: Experience,
    ) -> None:
        """
        Delete an experience.
        """

        super().delete(experience)