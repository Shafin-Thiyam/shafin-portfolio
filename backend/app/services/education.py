from sqlalchemy.orm import Session

from app.models import Education
from app.repositories import EducationRepository
from app.schemas import (
    EducationCreate,
    EducationUpdate,
)

class EducationService:
    """
    Service layer for education operations.
    """
    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize education service.
        """

        self.repository = EducationRepository(db)

    def get_all_educations(
        self,
    ) -> list[Education]:
        """
        Retrieve all education records.
        """

        return self.repository.get_all()

    def get_education(
        self,
        education_id: int,
    ) -> Education | None:
        """
        Retrieve education by ID.
        """

        return self.repository.get_by_id(education_id)

    def get_education_by_institution(
        self,
        institution: str,
    ) -> Education | None:
        """
        Retrieve education by institution.
        """

        return self.repository.get_by_institution(institution)

    def get_educations_by_degree(
        self,
        degree: str,
    ) -> list[Education]:
        """
        Retrieve education records by degree.
        """

        return self.repository.get_by_degree(degree)

    def get_education_by_institution_and_degree(
        self,
        institution: str,
        degree: str,
    ) -> Education | None:
        """
        Retrieve education by institution and degree.
        """

        return self.repository.get_by_institution_and_degree(
            institution,
            degree,
        )
    
    def get_educations_by_field_of_study(
        self,
        field_of_study: str,
    ) -> list[Education]:
        """
        Retrieve education records by field of study.
        """

        return self.repository.get_by_field_of_study(field_of_study)
     
    def create_education(
        self,
        education_data: EducationCreate,
    ) -> Education:
        """
        Create a new education record.
        """
        
        duplicate = self.repository.get_by_institution_and_degree(
            education_data.institution,
            education_data.degree,
        )
        

        if duplicate is not None:
            raise ValueError("Education already exists.")

        return self.repository.create(education_data)

    def update_education(
        self,
        education_id: int,
        updated_education: EducationUpdate,
    ) -> Education:
        """
        Update an existing education record.
        """

        existing_education = self.repository.get_by_id(
            education_id
        )

        if existing_education is None:
            raise ValueError("Education not found.")

        duplicate = self.repository.get_by_institution_and_degree(
            updated_education.institution,
            updated_education.degree,
        )

        if (
            duplicate is not None
            and duplicate.id != existing_education.id
        ):
            raise ValueError("Education already exists.")

        for field, value in updated_education.model_dump().items():
            setattr(
                existing_education,
                field,
                value,
            )

        return self.repository.update(
            existing_education
        )

    def delete_education(
        self,
        education_id: int,
    ) -> None:
        """
        Delete an education record.
        """

        existing_education = self.repository.get_by_id(
            education_id
        )

        if existing_education is None:
            raise ValueError("Education not found.")

        self.repository.delete(existing_education)