"""
Verify SkillRepository functionality.
"""

import sys

from app.db.session import SessionLocal
from app.models import Skill
from app.repositories import SkillRepository
from app.schemas import SkillCreate

def main() -> None:
    """
    Verify SkillRepository.
    """

    print("=" * 60)
    print("Skill Repository Verification")
    print("=" * 60)

    db = SessionLocal()

    try:

        repository = SkillRepository(db)

        print("✓ Repository created")

        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------

        existing_skills = repository.get_all()

        for skill in existing_skills:
            repository.delete(skill)

        print("✓ Existing skills cleaned")

        # ---------------------------------------------------------
        # Verify create()
        # ---------------------------------------------------------
        
        python = SkillCreate(
            name="Python",
            category="Backend",
            proficiency=95,
            display_order=1,
        )

        created = repository.create(python)

        assert created.id is not None

        print("✓ create()")

        # ---------------------------------------------------------
        # Verify get_by_id()
        # ---------------------------------------------------------

        skill = repository.get_by_id(created.id)

        assert skill is not None
        assert skill.name == "Python"

        print("✓ get_by_id()")

        # ---------------------------------------------------------
        # Verify get_all()
        # ---------------------------------------------------------

        skills = repository.get_all()

        assert len(skills) == 1
        assert skills[0].name == "Python"

        print("✓ get_all()")

        # ---------------------------------------------------------
        # Verify get_by_name()
        # ---------------------------------------------------------

        skill = repository.get_by_name("Python")

        assert skill is not None
        assert skill.name == "Python"

        print("✓ get_by_name()")

        # ---------------------------------------------------------
        # Verify get_by_category()
        # ---------------------------------------------------------

        backend_skills = repository.get_by_category("Backend")

        assert len(backend_skills) == 1
        assert backend_skills[0].name == "Python"

        print("✓ get_by_category()")

        # ---------------------------------------------------------
        # Verify update()
        # ---------------------------------------------------------

        created.name = "FastAPI"
        created.proficiency = 98
        created.display_order = 2

        updated = repository.update(created)

        assert updated.name == "FastAPI"
        assert updated.proficiency == 98
        assert updated.display_order == 2

        print("✓ update()")

        # ---------------------------------------------------------
        # Verify persisted update
        # ---------------------------------------------------------

        stored = repository.get_by_id(updated.id)

        assert stored is not None
        assert stored.name == "FastAPI"

        print("✓ Updated values verified")

        # ---------------------------------------------------------
        # Verify delete()
        # ---------------------------------------------------------

        repository.delete(updated)

        deleted = repository.get_by_id(updated.id)

        assert deleted is None

        print("✓ delete()")

        # ---------------------------------------------------------
        # Verify display order
        # ---------------------------------------------------------

        repository.create(
            SkillCreate(
                name="Docker",
                category="DevOps",
                proficiency=90,
                display_order=3,
            )
        )

        repository.create(
            SkillCreate(
                name="Python",
                category="Backend",
                proficiency=95,
                display_order=1,
            )
        )

        repository.create(
            SkillCreate(
                name="FastAPI",
                category="Backend",
                proficiency=98,
                display_order=2,
            )
        )

        skills = repository.get_all()

        assert [
            skill.display_order
            for skill in skills
        ] == [1, 2, 3]

        print("✓ Display order verified")

        # ---------------------------------------------------------
        # Verify category ordering
        # ---------------------------------------------------------

        backend = repository.get_by_category("Backend")

        assert len(backend) == 2

        assert [
            skill.display_order
            for skill in backend
        ] == [1, 2]

        print("✓ Category ordering verified")

        print()
        print("=" * 60)
        print("Repository Verification Summary")
        print("=" * 60)

        print("✓ create()")
        print("✓ get_by_id()")
        print("✓ get_all()")
        print("✓ get_by_name()")
        print("✓ get_by_category()")
        print("✓ update()")
        print("✓ delete()")
        print("✓ Display order verified")
        print("✓ Category ordering verified")

        print()
        print("🎉 All SkillRepository verification tests passed successfully.")

    except AssertionError as exc:

        print()
        print("❌ Repository verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    finally:
        db.close()

    print("=" * 60)
    print("Repository verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()