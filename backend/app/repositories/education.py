"""
Education repository.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Education
from app.schemas import EducationCreate

from .base import BaseRepository


class EducationRepository(BaseRepository[Education]):
    """
    Repository for Education model.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize repository.
        """
        super().__init__(db, Education)

    def create(
        self,
        education_data: EducationCreate,
    ) -> Education:
        """
        Create a new education.
        """

        education = Education(
            **education_data.model_dump(),
        )

        return super().create(education)

    def update(
        self,
        education: Education,
    ) -> Education:
        """
        Update an existing education.
        """

        return super().update(education)

    def delete(
        self,
        education: Education,
    ) -> None:
        """
        Delete an education.
        """

        super().delete(education)

    def get_by_id(
        self,
        education_id: int,
    ) -> Education | None:
        """
        Retrieve an education by ID.
        """

        return super().get_by_id(education_id)

    def get_all(self) -> list[Education]:
        """
        Retrieve all educations ordered by display order.
        """

        statement = (
            select(Education)
            .order_by(
                Education.display_order.asc(),
                Education.id.asc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_institution(
        self,
        institution: str,
    ) -> Education | None:
        """
        Retrieve an education by institution.
        """

        statement = (
            select(Education)
            .where(
                Education.institution == institution,
            )
        )

        return self.db.scalar(statement)

    def get_by_degree(
        self,
        degree: str,
    ) -> list[Education]:
        """
        Retrieve educations by degree.
        """

        statement = (
            select(Education)
            .where(
                Education.degree == degree,
            )
            .order_by(
                Education.display_order.asc(),
                Education.id.asc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_institution_and_degree(
        self,
        institution: str,
        degree: str,
    ) -> Education | None:
        """
        Retrieve an education by institution and degree.
        """
        
        statement = (
                    select(Education)
                    .where(
                        Education.institution == institution,
                        Education.degree == degree,
                    )
        )
        
        return self.db.scalar(statement)
    
    
    def get_by_field_of_study(
        self,
        field_of_study: str,
    ) -> list[Education]:
        """
        Retrieve educations by field of study.
        """

        statement = (
            select(Education)
            .where(
                Education.field_of_study == field_of_study,
            )
            .order_by(
                Education.display_order.asc(),
                Education.id.asc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )