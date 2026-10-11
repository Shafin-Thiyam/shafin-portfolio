"""
Experience service.
"""

from sqlalchemy.orm import Session

from app.models import Experience
from app.repositories import (
    ExperienceRepository,
    SkillRepository,
)

from app.schemas import (
    ExperienceCreate,
    ExperienceUpdate,
)

DUPLICATE_EXPERIENCE_MESSAGE = (
    "An experience with the same company, "
    "designation, and start date already exists."
)
EXPERIENCE_NOT_FOUND_MESSAGE = (
    "Experience not found."
)
SKILL_NOT_FOUND_MESSAGE = (
    "Skill not found."
)
EXPERIENCE_SKILL_ALREADY_EXISTS_MESSAGE = (
    "Skill is already associated with this experience."
)
EXPERIENCE_SKILL_NOT_FOUND_MESSAGE = (
    "Skill is not associated with this experience."
)


class ExperienceService:
    """
    Service layer for experience operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize experience service.
        """
        
        self.repository = ExperienceRepository(db)
        self.skill_repository = SkillRepository(db)

    def _is_duplicate(
        self,
        experience_data: ExperienceCreate | ExperienceUpdate,
        exclude_id: int | None = None,
    ) -> bool:
        """
        Check whether an equivalent experience already exists.

        An experience is considered a duplicate when another
        experience has the same company, designation, and
        start date.

        Args:
            experience_data:
                Experience data being created or updated.

            exclude_id:
                Experience ID to exclude during update operations.

        Returns:
            True if a duplicate exists, otherwise False.
        """

        experiences = self.repository.get_by_company(
            experience_data.company
        )

        for experience in experiences:
            if (
                exclude_id is not None
                and experience.id == exclude_id
            ):
                continue

            if (
                experience.designation.casefold()
                == experience_data.designation.casefold()
                and experience.start_date
                == experience_data.start_date
            ):
                return True

        return False
    
    # =========================================================
    # Retrieval
    # =========================================================

    def get_all(self) -> list[Experience]:
        """
        Retrieve all experiences ordered by display order.
        """

        return self.repository.get_all()

    def get_by_id(
        self,
        experience_id: int,
    ) -> Experience | None:
        """
        Retrieve an experience by ID.
        """

        return self.repository.get_by_id(
            experience_id
        )
    
    def get_filtered(
        self,
        company: str | None = None,
        employment_type: str | None = None,
        location_type: str | None = None,
    ) -> list[Experience]:
        return self.repository.get_filtered(
            company=company,
            employment_type=employment_type,
            location_type=location_type,
        )
    
    def get_current(self) -> list[Experience]:
        """
        Retrieve current experiences ordered by display order.
        """

        return self.repository.get_current()

    def get_by_company(
        self,
        company: str,
    ) -> list[Experience]:
        """
        Retrieve experiences by company.

        Matching is case-insensitive.
        """

        return self.repository.get_by_company(
            company
        )

    def get_by_employment_type(
        self,
        employment_type: str,
    ) -> list[Experience]:
        """
        Retrieve experiences by employment type.

        Matching is case-insensitive.
        """

        return self.repository.get_by_employment_type(
            employment_type
        )

    def get_by_location_type(
        self,
        location_type: str,
    ) -> list[Experience]:
        """
        Retrieve experiences by location type.

        Matching is case-insensitive.
        """

        return self.repository.get_by_location_type(
            location_type
        )
    
    # =========================================================
    # CRUD
    # =========================================================

    def create(
        self,
        experience_data: ExperienceCreate,
    ) -> Experience:
        """
        Create a new experience.
        """
        if self._is_duplicate(experience_data):
            raise ValueError(DUPLICATE_EXPERIENCE_MESSAGE)

        return self.repository.create(
            experience_data
        )

    def update(
        self,
        experience_id: int,
        experience_data: ExperienceUpdate,
    ) -> Experience:
        """
        Update an existing experience.
        """

        existing_experience = self.repository.get_by_id(
            experience_id
        )

        if existing_experience is None:
            raise ValueError(EXPERIENCE_NOT_FOUND_MESSAGE)
        
        if self._is_duplicate(
            experience_data,
            exclude_id=experience_id,
        ):
            raise ValueError(DUPLICATE_EXPERIENCE_MESSAGE)

        for field, value in experience_data.model_dump().items():
            setattr(
                existing_experience,
                field,
                value,
            )

        return self.repository.update(
            existing_experience
        )

    def delete(
        self,
        experience_id: int,
    ) -> None:
        """
        Delete an experience.
        """

        existing_experience = self.repository.get_by_id(
            experience_id
        )

        if existing_experience is None:
            raise ValueError(EXPERIENCE_NOT_FOUND_MESSAGE)

        self.repository.delete(
            existing_experience
        )

    # =========================================================
    # Skill Queries
    # =========================================================
    
    def get_by_skill_id(
        self,
        skill_id: int,
    ) -> list[Experience]:
        """
        Retrieve experiences associated with a skill ID.

        Results are ordered by display order.
        """

        return self.repository.get_by_skill_id(
            skill_id
        )

    def get_by_skill_name(
        self,
        skill_name: str,
    ) -> list[Experience]:
        """
        Retrieve experiences associated with a skill name.

        Matching is case-insensitive.

        Results are ordered by display order.
        """

        return self.repository.get_by_skill_name(
            skill_name
        )

    def get_skill_ids(
        self,
        experience_id: int,
    ) -> list[int]:
        """
        Retrieve skill IDs associated with an experience.
        """
        
        existing_experience = self.repository.get_by_id(
            experience_id
            )
        
        if existing_experience is None:
            raise ValueError(
                EXPERIENCE_NOT_FOUND_MESSAGE
                )

        return self.repository.get_skill_ids(
            experience_id
        )
        
    # =========================================================
    # Skill Management
    # =========================================================
        
    def add_skill(
        self,
        experience_id: int,
        skill_id: int,
    ) -> None:
        """
        Associate a skill with an experience.

        Raises:
            ValueError:
                If the experience does not exist.
            ValueError:
                If the skill does not exist.
            ValueError:
                If the skill is already associated.
        """

        existing_experience = self.repository.get_by_id(
            experience_id
        )

        if existing_experience is None:
            raise ValueError(
                EXPERIENCE_NOT_FOUND_MESSAGE
            )

        existing_skill = self.skill_repository.get_by_id(
            skill_id
        )

        if existing_skill is None:
            raise ValueError(
                SKILL_NOT_FOUND_MESSAGE
            )

        existing_skill_ids = self.repository.get_skill_ids(
            experience_id
        )

        if skill_id in existing_skill_ids:
            raise ValueError(
                EXPERIENCE_SKILL_ALREADY_EXISTS_MESSAGE
            )

        self.repository.add_skill(
            experience_id,
            skill_id,
        )
             
    def remove_skill(
        self,
        experience_id: int,
        skill_id: int,
    ) -> None:
        
        """
        Remove a skill association from an experience.

        Raises:
            ValueError:
                If the experience does not exist.
            ValueError:
                If the skill does not exist.
            ValueError:
                If the skill is not associated with the experience.
        """

        existing_experience = self.repository.get_by_id(
            experience_id
        )

        if existing_experience is None:
            raise ValueError(
                EXPERIENCE_NOT_FOUND_MESSAGE
            )

        existing_skill = self.skill_repository.get_by_id(
            skill_id
        )

        if existing_skill is None:
            raise ValueError(
                SKILL_NOT_FOUND_MESSAGE
            )

        existing_skill_ids = self.repository.get_skill_ids(
            experience_id
        )

        if skill_id not in existing_skill_ids:
            raise ValueError(
                EXPERIENCE_SKILL_NOT_FOUND_MESSAGE
            )

        self.repository.remove_skill(
            experience_id,
            skill_id,
        )
            
    def set_skills(
        self,
        experience_id: int,
        skill_ids: list[int],
    ) -> None:
        
        """
        Replace all skill associations for an experience.

        All supplied skill IDs must exist before any
        relationship changes are made.

        Raises:
            ValueError:
                If the experience does not exist.
            ValueError:
                If one or more skills do not exist.
        """

        existing_experience = self.repository.get_by_id(
            experience_id
        )

        if existing_experience is None:
            raise ValueError(
                EXPERIENCE_NOT_FOUND_MESSAGE
            )

        unique_skill_ids = list(
            dict.fromkeys(skill_ids)
        )

        for skill_id in unique_skill_ids:
            existing_skill = self.skill_repository.get_by_id(
                skill_id
            )

            if existing_skill is None:
                raise ValueError(
                    SKILL_NOT_FOUND_MESSAGE
                )

        self.repository.set_skills(
            experience_id,
            unique_skill_ids,
        )
        
    def clear_skills(
        self,
        experience_id: int,
    ) -> None:
        """
        Remove all skill associations from an experience.

        Raises:
            ValueError:
                If the experience does not exist.
        """

        existing_experience = self.repository.get_by_id(
            experience_id
        )

        if existing_experience is None:
            raise ValueError(
                EXPERIENCE_NOT_FOUND_MESSAGE
            )

        self.repository.clear_skills(
            experience_id
        )