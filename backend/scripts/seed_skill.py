"""
Seed portfolio skills.
"""

import sys

from app.db.session import SessionLocal
from app.schemas import SkillCreate
from app.services import SkillService


SKILLS = [
    SkillCreate(
        name="Python",
        category="Programming",
        proficiency=95,
        display_order=1,
    ),
    SkillCreate(
        name="XSL",
        category="Programming",
        proficiency=95,
        display_order=2,
    ),
    SkillCreate(
        name="FastAPI",
        category="Backend",
        proficiency=74,
        display_order=3,
    ),
    SkillCreate(
        name="Flask",
        category="Backend",
        proficiency=72,
        display_order=4,
    ),
    SkillCreate(
        name="Django",
        category="Backend",
        proficiency=67,
        display_order=5,
    ),
    SkillCreate(
        name="PostgreSQL",
        category="Database",
        proficiency=85,
        display_order=6,
    ),
    SkillCreate(
        name="SAP BTP",
        category="Cloud",
        proficiency=90,
        display_order=7,
    ),
    SkillCreate(
        name="Docker",
        category="DevOps",
        proficiency=85,
        display_order=8,
    ),
    SkillCreate(
        name="Kubernetes",
        category="DevOps",
        proficiency=80,
        display_order=9,
    ),
    SkillCreate(
        name="Kafka",
        category="Messaging",
        proficiency=32,
        display_order=10,
    ),
    SkillCreate(
        name="Git",
        category="Tools",
        proficiency=75,
        display_order=11,
    ),
    SkillCreate(
        name="Linux",
        category="Tools",
        proficiency=85,
        display_order=12,
    ),
    SkillCreate(
        name="AWS",
        category="Cloud",
        proficiency=65,
        display_order=13,
    ),
]


def main() -> None:
    """
    Seed portfolio skills.
    """

    print("=" * 60)
    print("Skill Seed")
    print("=" * 60)

    db = SessionLocal()

    try:
        service = SkillService(db)

        created = 0
        skipped = 0

        for skill in SKILLS:

            existing = service.get_skill_by_name(skill.name)

            if existing is not None:
                print(f"• Skipped : {skill.name}")
                skipped += 1
                continue

            service.create_skill(skill)

            print(f"✓ Created : {skill.name}")
            created += 1

        print()
        print("=" * 60)
        print("Seed Summary")
        print("=" * 60)
        print(f"Created : {created}")
        print(f"Skipped : {skipped}")

    except Exception as exc:
        print()
        print("❌ Skill seed failed")
        print(exc)
        sys.exit(1)

    finally:
        db.close()

    print("=" * 60)
    print("Skill seeding completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()