"""
Seed education data.
"""

from datetime import date
import sys

from app.db.session import SessionLocal
from app.schemas import EducationCreate
from app.services import EducationService


EDUCATIONS = [
    EducationCreate(
        institution="Mumbai University",
        degree="M.C.A",
        field_of_study="Computer",
        start_date=date(2005, 6, 1),
        end_date=date(2008, 5, 31),
        grade="tofill %",
        description="The Master of Computer Applications (MCA) degree from the University of Mumbai in 2005 was a 3-year postgraduate program focused on software development and computer systems.",
        display_order= 1
    ),
    EducationCreate(
        institution="Mumbai University",
        degree="B.Sc.IT",
        field_of_study="Computer",
        start_date=date(2002, 6, 1),
        end_date=date(2005, 5, 31),
        grade="to fill %",
        description="The University of Mumbai introduced the Bachelor of Science in Information Technology (B.Sc. IT) degree in 2002 to build strong student skills in programming, databases, and core computer applications.",
        display_order=2
    ),
]


def main() -> None:
    """
    Seed portfolio Educations.
    """

    print("=" * 60)
    print("Education Seed")
    print("=" * 60)

    db = SessionLocal()

    try:
        service = EducationService(db)

        created = 0
        skipped = 0

        for education in EDUCATIONS:

            existing = service.get_education_by_institution_and_degree(
                education.institution,
                education.degree   
            )

            if existing is not None:
                print(f"• Skipped : {education.degree}")
                skipped += 1
                continue

            service.create_education(education)

            print(f"✓ Created : {education.degree}")
            created += 1

        print()
        print("=" * 60)
        print("Seed Summary")
        print("=" * 60)
        print(f"Created : {created}")
        print(f"Skipped : {skipped}")

    except Exception as exc:
        print()
        print("❌ Education seed failed")
        print(exc)
        sys.exit(1)

    finally:
        db.close()

    print("=" * 60)
    print("Education seeding completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()