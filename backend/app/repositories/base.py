"""
Generic repository foundation.

This module provides the reusable BaseRepository used by all
application repositories. It implements common CRUD operations
for SQLAlchemy ORM models.
"""

from typing import Any, Generic, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import Base

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)

class BaseRepository(Generic[ModelType]):
    """
    Base repository for SQLAlchemy models.
    """
    def __init__(
        self,
        db: Session,
        model: Type[ModelType],
    ) -> None:
        
        """
        Initialize repository.

        Args:
            db:
                Active SQLAlchemy session.

            model:
                SQLAlchemy model handled by this repository.
        """

        self.db = db
        self.model = model
    
    def create(
        self,
        obj: ModelType,
    ) -> ModelType:
        
        """
        Persist a new entity.

        Args:
            obj:
                SQLAlchemy model instance.

        Returns:
            Persisted model instance.
        """

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj
    
    def get_by_id(
        self,
        obj_id: Any,
    ) -> ModelType | None:
        
        """
        Retrieve an entity by its primary key.

        Args:
            obj_id:
                Primary key value.

        Returns:
            Model instance or None.
        """

        return self.db.get(
            self.model,
            obj_id,
        )
        
    def get_all(self) -> list[ModelType]:
        """
        Retrieve all entities.

        Returns:
            List of model instances.
        """

        statement = select(self.model)

        return list(
            self.db.scalars(statement).all()
        )
    
    def update(
        self,
        obj: ModelType,
    ) -> ModelType:
    
        """
        Update an existing entity.

        Args:
            obj:
                SQLAlchemy model instance.

        Returns:
            Updated model instance.
        """

        obj = self.db.merge(obj)

        self.db.commit()

        self.db.refresh(obj)

        return obj
    
    def delete(
        self,
        obj: ModelType,
    ) -> None:
        """
        Delete an entity.

        Args:
            obj:
                SQLAlchemy model instance.
        """

        self.db.delete(obj)

        self.db.commit()
        
    def exists(
        self,
        obj_id: Any,
    ) -> bool:
        
        """
        Check whether an entity exists.

        Args:
            obj_id:
                Primary key value.

        Returns:
            True if the entity exists, otherwise False.
        """

        return self.get_by_id(obj_id) is not None
    
    def count(self) -> int:
    
        """
        Return the total number of entities.

        Returns:
            Total number of records.
        """

        statement = select(
            func.count()
        ).select_from(self.model)

        return self.db.scalar(statement) or 0

    