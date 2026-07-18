"""
Skill service.
"""

from sqlalchemy.orm import Session

from app.models import Skill
from app.repositories import SkillRepository
from app.schemas import (
    SkillCreate,
    SkillUpdate,
)


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
        skill: SkillCreate,
    ) -> Skill:
        """
        Create a new skill.
        """

        if self.repository.get_by_name(skill.name):
            raise ValueError("Skill already exists.")

        new_skill = Skill(
            name=skill.name,
            category=skill.category,
            proficiency=skill.proficiency,
            display_order=skill.display_order,
        )

        return self.repository.create(new_skill)

    def update_skill(
        self,
        skill_id: int,
        skill: SkillUpdate,
    ) -> Skill:
        """
        Update an existing skill.
        """

        existing_skill = self.repository.get_by_id(skill_id)

        if existing_skill is None:
            raise ValueError("Skill not found.")

        if existing_skill.name != skill.name:

            duplicate = self.repository.get_by_name(skill.name)

            if duplicate:
                raise ValueError("Skill already exists.")

        existing_skill.name = skill.name
        existing_skill.category = skill.category
        existing_skill.proficiency = skill.proficiency
        existing_skill.display_order = skill.display_order

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