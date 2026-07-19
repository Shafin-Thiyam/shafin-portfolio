"""
Verify seeded portfolio skills.
"""

import sys

from app.db.session import SessionLocal
from app.services import SkillService


EXPECTED_SKILLS = {
    "Python",
    "XSL",
    "FastAPI",
    "Flask",
    "Django",
    "PostgreSQL",
    "SAP BTP",
    "Docker",
    "Kubernetes",
    "Kafka",
    "Git",
    "Linux",
    "AWS",
}

EXPECTED_CATEGORIES = {
    "Programming",
    "Backend",
    "Database",
    "Cloud",
    "DevOps",
    "Messaging",
    "Tools",
}


def main() -> None:
    """
    Verify seeded skills.
    """

    print("=" * 60)
    print("Skill Seed Verification")
    print("=" * 60)

    db = SessionLocal()

    try:
        service = SkillService(db)

        print("✓ Service created")

        # ---------------------------------------------------------
        # Retrieve all skills
        # ---------------------------------------------------------

        skills = service.get_all_skills()

        # ---------------------------------------------------------
        # Verify total count
        # ---------------------------------------------------------

        assert len(skills) == len(EXPECTED_SKILLS)

        print(f"✓ Total skills: {len(skills)}")

        # ---------------------------------------------------------
        # Verify display order
        # ---------------------------------------------------------

        display_orders = [
            skill.display_order
            for skill in skills
        ]

        assert display_orders == sorted(display_orders)

        print("✓ Display order verified")

        # ---------------------------------------------------------
        # Verify unique names
        # ---------------------------------------------------------

        names = [
            skill.name
            for skill in skills
        ]

        assert len(names) == len(set(names))

        print("✓ Unique skill names")

        # ---------------------------------------------------------
        # Verify expected skills
        # ---------------------------------------------------------

        assert set(names) == EXPECTED_SKILLS

        print("✓ Expected skills verified")

        # ---------------------------------------------------------
        # Verify categories
        # ---------------------------------------------------------

        categories = {
            skill.category
            for skill in skills
        }

        assert EXPECTED_CATEGORIES.issubset(categories)

        print("✓ Categories verified")

        # ---------------------------------------------------------
        # Verify lookup by name
        # ---------------------------------------------------------

        for name in EXPECTED_SKILLS:

            skill = service.get_skill_by_name(name)

            assert skill is not None
            assert skill.name == name

        print("✓ Lookup by name verified")

        # ---------------------------------------------------------
        # Verify lookup by category
        # ---------------------------------------------------------

        for category in EXPECTED_CATEGORIES:

            category_skills = service.get_skills_by_category(category)

            assert len(category_skills) > 0

        print("✓ Lookup by category verified")

        # ---------------------------------------------------------
        # Verify timestamps
        # ---------------------------------------------------------

        for skill in skills:

            assert skill.created_at is not None
            assert skill.updated_at is not None

        print("✓ Timestamps verified")

        print()
        print("=" * 60)
        print("Seed Verification Summary")
        print("=" * 60)

        print(f"✓ {len(skills)} skills verified")
        print("✓ Display order verified")
        print("✓ Unique names verified")
        print("✓ Expected skills verified")
        print("✓ Categories verified")
        print("✓ Name lookup verified")
        print("✓ Category lookup verified")
        print("✓ Timestamps verified")

        print()
        print("🎉 All seeded skills verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ Seed verification failed")
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
    print("Seed verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()