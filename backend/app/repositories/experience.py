"""
Experience repository.
"""

from sqlalchemy import (
    select,
    func,
)
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

    def get_current(self) -> list[Experience]:
        """
        Retrieve current experiences ordered by display order.
        """

        statement = (
            select(Experience)
            .where(
                Experience.is_current.is_(True)
            )
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_company(
        self,
        company: str,
    ) -> list[Experience]:
        """
        Retrieve experiences for a company.

        Matching is case-insensitive.
        """

        statement = (
            select(Experience)
            .where(
                func.lower(Experience.company)
                == company.lower()
            )
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_employment_type(
        self,
        employment_type: str,
    ) -> list[Experience]:
        """
        Retrieve experiences by employment type.

        Matching is case-insensitive.
        """

        statement = (
            select(Experience)
            .where(
                func.lower(Experience.employment_type)
                == employment_type.lower()
            )
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_location_type(
        self,
        location_type: str,
    ) -> list[Experience]:
        """
        Retrieve experiences by location type.

        Matching is case-insensitive.
        """

        statement = (
            select(Experience)
            .where(
                func.lower(Experience.location_type)
                == location_type.lower()
            )
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
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