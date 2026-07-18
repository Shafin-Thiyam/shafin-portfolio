"""
Skill service.
"""

from sqlalchemy.orm import Session

from app.models import Skill
from app.repositories import SkillRepository
#from app.schemas import (
#    SkillCreate,
#    SkillUpdate,
#)


class SkillService:
    """
    Service layer for skill operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize skill service.
        """

        self.repository = SkillRepository(db)

    def get_all_skills(self) -> list[Skill]:
        """
        Retrieve all skills.
        """

        return self.repository.get_all()

    def get_skill(
        self,
        skill_id: int,
    ) -> Skill | None:
        """
        Retrieve a skill by ID.
        """

        return self.repository.get_by_id(skill_id)

    def get_skill_by_name(
        self,
        name: str,
    ) -> Skill | None:
        """
        Retrieve a skill by name.
        """

        return self.repository.get_by_name(name)

    def get_skills_by_category(
        self,
        category: str,
    ) -> list[Skill]:
        """
        Retrieve all skills in a category.
        """

        return self.repository.get_by_category(category)

    def create_skill(
        self,
        skill: Skill,
    ) -> Skill:
        """ 
        Create a new skill.
        """

        duplicate = self.repository.get_by_name(skill.name)

        if duplicate is not None:
            raise ValueError("Skill already exists.")
        

        return self.repository.create(skill)

    def update_skill(
        self,
        skill_id: int,
        updated_skill: Skill,
    ) -> Skill:
        """
        Update an existing skill.
        """

        existing_skill = self.repository.get_by_id(skill_id)

        if existing_skill is None:
            raise ValueError("Skill not found.")

        if existing_skill.name != updated_skill.name:

            duplicate = self.repository.get_by_name(updated_skill.name)

            if duplicate is not None:
                raise ValueError("Skill already exists.")

        existing_skill.name = updated_skill.name
        existing_skill.category = updated_skill.category
        existing_skill.proficiency = updated_skill.proficiency
        existing_skill.display_order = updated_skill.display_order

        return self.repository.update(existing_skill)

    def delete_skill(
        self,
        skill_id: int,
    ) -> None:
        """
        Delete a skill.
        """

        existing_skill = self.repository.get_by_id(skill_id)

        if existing_skill is None:
            raise ValueError("Skill not found.")

        self.repository.delete(existing_skill)