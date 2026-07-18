"""
Verify ProfileService functionality.
"""

import sys

from app.db.session import SessionLocal
from app.models import Skill
from app.services import SkillService


def main() -> None:
    """
    Verify SkillService.
    """

    print("=" * 60)
    print("Skill Service Verification")
    print("=" * 60)

    db = SessionLocal()

    try:
        service = SkillService(db)

        print("✓ Service created successfully")
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------

        for skill in service.get_all_skills():
            service.delete_skill(skill.id)

        print("✓ Existing skills cleaned")
        
        # ---------------------------------------------------------
        # Create Skill
        # ---------------------------------------------------------

        skill = Skill(
            name="Python",
            category="Backend",
            proficiency=95,
            display_order=1,
        )

        created_skill = service.create_skill(skill)

        assert created_skill.id is not None
        assert created_skill.name == "Python"
        assert created_skill.category == "Backend"

        print("✓ create_skill()")
        print(f"  ID: {created_skill.id}")
        
        stored_skill = service.get_skill(created_skill.id)

        assert stored_skill is not None
        assert stored_skill.name == created_skill.name

        print("✓ Skill persisted")
        # ---------------------------------------------------------
        # Verify get_skill()
        # ---------------------------------------------------------

        stored_skill = service.get_skill(created_skill.id)

        assert stored_skill is not None
        assert stored_skill.id == created_skill.id
        assert stored_skill.name == created_skill.name

        print("✓ get_skill()")
        
        # ---------------------------------------------------------
        # Verify get_skill_by_name()
        # ---------------------------------------------------------

        stored_skill = service.get_skill_by_name(created_skill.name)

        assert stored_skill is not None
        assert stored_skill.name == created_skill.name

        print("✓ get_skill_by_name()")
        
        # ---------------------------------------------------------
        # Verify get_all_skills()
        # ---------------------------------------------------------

        skills = service.get_all_skills()

        assert len(skills) == 1
        assert skills[0].name == created_skill.name

        print("✓ get_all_skills()")
        
        # ---------------------------------------------------------
        # Verify get_skills_by_category()
        # ---------------------------------------------------------

        backend_skills = service.get_skills_by_category(created_skill.category)

        assert len(backend_skills) == 1
        assert backend_skills[0].name == created_skill.name

        print("✓ get_skills_by_category()")
        
        # ---------------------------------------------------------
        # Verify duplicate skill creation
        # ---------------------------------------------------------

        duplicate_skill = Skill(
            name=created_skill.name,
            category="Backend",
            proficiency=90,
            display_order=99,
        )

        try:
            service.create_skill(duplicate_skill)
            raise AssertionError("Expected ValueError")

        except ValueError as exc:
            assert str(exc) == "Skill already exists."

        print("✓ Duplicate skill validation")
        
        
        # ---------------------------------------------------------
        # Verify update_skill()
        # ---------------------------------------------------------

        updated_skill = Skill(
            name="FastAPI",
            category="Backend",
            proficiency=98,
            display_order=2,
        )

        updated = service.update_skill(
            created_skill.id,
            updated_skill,
        )

        assert updated.name == updated_skill.name
        assert updated.category == updated_skill.category
        assert updated.proficiency == updated_skill.proficiency
        assert updated.display_order == updated_skill.display_order

        print("✓ update_skill()")
    
        # ---------------------------------------------------------
        # Verify updated values
        # ---------------------------------------------------------

        stored_skill = service.get_skill(created_skill.id)

        assert stored_skill is not None
        assert stored_skill.name == updated_skill.name
        assert stored_skill.category == updated_skill.category
        assert stored_skill.proficiency == updated_skill.proficiency
        assert stored_skill.display_order == updated_skill.display_order

        print("✓ Updated values verified")
        
        # ---------------------------------------------------------
        # Verify get_skill_by_name() after update
        # ---------------------------------------------------------

        stored_skill = service.get_skill_by_name(updated_skill.name)

        assert stored_skill is not None
        assert stored_skill.id == created_skill.id

        print("✓ get_skill_by_name() after update")
        
        # ---------------------------------------------------------
        # Verify delete_skill()
        # ---------------------------------------------------------

        service.delete_skill(created_skill.id)

        print("✓ delete_skill()")
        
        # ---------------------------------------------------------
        # Verify get_skill() after delete
        # ---------------------------------------------------------

        deleted_skill = service.get_skill(created_skill.id)

        assert deleted_skill is None

        print("✓ get_skill() after delete")
        
        # ---------------------------------------------------------
        # Verify get_skill_by_name() after delete
        # ---------------------------------------------------------

        deleted_skill = service.get_skill_by_name(updated_skill.name)

        assert deleted_skill is None

        print("✓ get_skill_by_name() after delete")
        
        # ---------------------------------------------------------
        # Verify get_all_skills() after delete
        # ---------------------------------------------------------

        skills = service.get_all_skills()

        assert len(skills) == 0

        print("✓ get_all_skills() after delete")
        
        # ---------------------------------------------------------
        # Verify get_skills_by_category() after delete
        # ---------------------------------------------------------

        backend_skills = service.get_skills_by_category("Backend")

        assert len(backend_skills) == 0

        print("✓ get_skills_by_category() after delete")
        
        # ---------------------------------------------------------
        # Verify update non-existent skill
        # ---------------------------------------------------------

        missing_skill = Skill(
            name="Docker",
            category="DevOps",
            proficiency=85,
            display_order=3,
        )

        try:
            service.update_skill(999999, missing_skill)
            raise AssertionError("Expected ValueError")

        except ValueError as exc:
            assert str(exc) == "Skill not found."

        print("✓ Update missing skill validation")
        
        # ---------------------------------------------------------
        # Verify delete non-existent skill
        # ---------------------------------------------------------

        try:
            service.delete_skill(999999)
            raise AssertionError("Expected ValueError")

        except ValueError as exc:
            assert str(exc) == "Skill not found."

        print("✓ Delete missing skill validation")
        
        # ---------------------------------------------------------
        # Verify duplicate name on update
        # ---------------------------------------------------------

        python_skill = service.create_skill(
            Skill(
                name="Python",
                category="Backend",
                proficiency=95,
                display_order=1,
            )
        )

        docker_skill = service.create_skill(
            Skill(
                name="Docker",
                category="DevOps",
                proficiency=90,
                display_order=2,
            )
        )

        duplicate_update = Skill(
            name="Python",
            category="DevOps",
            proficiency=90,
            display_order=2,
        )

        try:
            service.update_skill(
                docker_skill.id,
                duplicate_update,
            )
            raise AssertionError("Expected ValueError")

        except ValueError as exc:
            assert str(exc) == "Skill already exists."

        print("✓ Duplicate update validation")
        
        print()
        print("=" * 60)
        print("Skill Service Verification Summary")
        print("=" * 60)

        print("✓ create_skill()")
        print("✓ get_skill()")
        print("✓ get_skill_by_name()")
        print("✓ get_all_skills()")
        print("✓ get_skills_by_category()")
        print("✓ update_skill()")
        print("✓ delete_skill()")
        print("✓ Duplicate create validation")
        print("✓ Update missing skill validation")
        print("✓ Delete missing skill validation")
        print("✓ Duplicate update validation")

        print()
        print("🎉 All SkillService verification tests passed successfully.")
        print("=" * 60)

    except AssertionError as exc:
        print()
        print("❌ Service verification failed")
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
    print("Verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()