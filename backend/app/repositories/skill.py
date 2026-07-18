"""
Skill repository.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Skill

from .base import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    """
    Repository for Skill model.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize repository.
        """
        super().__init__(db, Skill)

    def create(self, skill: Skill) -> Skill:
        """
        Create a new skill.
        """
        return super().create(skill)

    def update(self, skill: Skill) -> Skill:
        """
        Update an existing skill.
        """
        return super().update(skill)

    def delete(self, skill: Skill) -> None:
        """
        Delete a skill.
        """
        super().delete(skill)

    def get_by_id(self, skill_id: int) -> Skill | None:
        """
        Retrieve a skill by ID.
        """
        return super().get_by_id(skill_id)

    def get_all(self) -> list[Skill]:
        """
        Retrieve all skills ordered by display order.
        """
        statement = (
            select(Skill)
            .order_by(
                Skill.display_order.asc(),
                Skill.id.asc(),
            )
        )

        return list(self.db.scalars(statement).all())

    def get_by_name(self, name: str) -> Skill | None:
        """
        Retrieve a skill by name.
        """
        statement = (
            select(Skill)
            .where(Skill.name == name)
        )

        return self.db.scalar(statement)

    def get_by_category(
        self,
        category: str,
    ) -> list[Skill]:
        """
        Retrieve all skills in a category.
        """
        statement = (
            select(Skill)
            .where(Skill.category == category)
            .order_by(
                Skill.display_order.asc(),
                Skill.id.asc(),
            )
        )

        return list(self.db.scalars(statement).all())