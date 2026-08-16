"""
Experience repository.
"""

from sqlalchemy import (
    select,
    func,
)
from sqlalchemy.orm import Session

from app.models import (
    Experience,
    Skill,
    experience_skills,
)

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

    def get_by_skill_id(
        self,
        skill_id: int,
    ) -> list[Experience]:
        """
        Retrieve experiences associated with a skill.

        Results are ordered by display order.
        """

        statement = (
            select(Experience)
            .join(
                experience_skills,
                Experience.id
                == experience_skills.c.experience_id,
            )
            .where(
                experience_skills.c.skill_id
                == skill_id
            )
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
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

        statement = (
            select(Experience)
            .join(
                experience_skills,
                Experience.id
                == experience_skills.c.experience_id,
            )
            .join(
                Skill,
                Skill.id
                == experience_skills.c.skill_id,
            )
            .where(
                func.lower(Skill.name)
                == skill_name.lower()
            )
            .order_by(
                Experience.display_order.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_skill_ids(
        self,
        experience_id: int,
    ) -> list[int]:
        """
        Retrieve skill IDs associated with an experience.
        """

        statement = (
            select(
                experience_skills.c.skill_id
            )
            .where(
                experience_skills.c.experience_id
                == experience_id
            )
            .order_by(
                experience_skills.c.skill_id.asc()
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
        
    def add_skill(
        self,
        experience_id: int,
        skill_id: int,
    ) -> None:
        """
        Associate a skill with an experience.
        """

        statement = (
            select(experience_skills.c.experience_id)
            .where(
                experience_skills.c.experience_id
                == experience_id,
                experience_skills.c.skill_id
                == skill_id,
            )
        )

        exists = self.db.scalar(statement)

        if exists is not None:
            return

        self.db.execute(
            experience_skills.insert().values(
                experience_id=experience_id,
                skill_id=skill_id,
            )
        )

        self.db.flush()
    
    def remove_skill(
        self,
        experience_id: int,
        skill_id: int,
    ) -> None:
        """
        Remove a skill association from an experience.
        """

        statement = (
            experience_skills.delete()
            .where(
                experience_skills.c.experience_id
                == experience_id,
                experience_skills.c.skill_id
                == skill_id,
            )
        )

        self.db.execute(statement)
        self.db.flush()
        
    def set_skills(
        self,
        experience_id: int,
        skill_ids: list[int],
    ) -> None:
        """
        Replace all skill associations for an experience.
        """

        self.clear_skills(experience_id)

        if not skill_ids:
            return

        rows = [
            {
                "experience_id": experience_id,
                "skill_id": skill_id,
            }
            for skill_id in dict.fromkeys(skill_ids)
        ]

        self.db.execute(
            experience_skills.insert(),
            rows,
        )

        self.db.flush()
        
    def clear_skills(
        self,
        experience_id: int,
    ) -> None:
        """
        Remove all skill associations from an experience.
        """

        statement = (
            experience_skills.delete()
            .where(
                experience_skills.c.experience_id
                == experience_id
            )
        )

        self.db.execute(statement)
        self.db.flush()