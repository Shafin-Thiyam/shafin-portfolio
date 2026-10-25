import sys
from datetime import date

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Experience, Project
from app.schemas import ProjectCreate
from app.services import ProjectService


PROJECTS = [
    {
        "company": "Tata Consultancy Services (TCS)",
        "designation": "Associate Consultant",
        "experience_start_date": date(2022, 9, 1),
        "title": "SAP AI Core Lifecycle Management",
        "description": (
            "Migrated SAP Data Intelligence applications to SAP AI Core, "
            "supporting their transition from proof of concept to production. "
            "Worked on lifecycle management practices for tracking, deploying, "
            "and managing machine learning artifacts."
        ),
        "role": "Python Developer / Cloud Solutions",
        "technologies": [
            "Python",
            "SAP AI Core",
            "SAP AI Launchpad",
            "SAP Data Intelligence",
            "Docker",
            "Kubernetes",
        ],
        "project_url": None,
        "repository_url": None,
        "start_date": None,
        "end_date": None,
        "display_order": 1,
    },
    {
        "company": "Tata Consultancy Services (TCS)",
        "designation": "Associate Consultant",
        "experience_start_date": date(2022, 9, 1),
        "title": "SAP BTP Audit and Usage Log Integration",
        "description": (
            "Developed an integration to route SAP BTP audit and usage logs "
            "through AEM to Kafka, supporting downstream log processing."
        ),
        "role": "Python Developer / Cloud Integration",
        "technologies": [
            "Python",
            "SAP BTP",
            "AEM",
            "Kafka",
            "REST APIs",
        ],
        "project_url": None,
        "repository_url": None,
        "start_date": None,
        "end_date": None,
        "display_order": 2,
    },
    {
        "company": "Thomson Reuters",
        "designation": "Senior Software Engineer",
        "experience_start_date": date(2016, 6, 1),
        "title": "Python XML Transformation API",
        "description": (
            "Developed a Flask REST API that accepts XML input, executes "
            "specified XSL stylesheets, and returns transformed XML output "
            "in JSON format."
        ),
        "role": "Python Developer",
        "technologies": [
            "Python",
            "Flask",
            "REST APIs",
            "XML",
            "XSLT",
            "XSD",
        ],
        "project_url": None,
        "repository_url": None,
        "start_date": None,
        "end_date": None,
        "display_order": 1,
    },
]


def find_experience(
    db,
    company: str,
    designation: str,
    start_date: date,
) -> Experience | None:
    """Find an experience using its natural identifying fields."""

    statement = select(Experience).where(
        Experience.company.ilike(company),
        Experience.designation.ilike(designation),
        Experience.start_date == start_date,
    )

    return db.scalars(statement).first()


def main() -> None:
    """Seed projects without creating duplicates."""

    print("=" * 60)
    print("Project Seed")
    print("=" * 60)

    db = SessionLocal()
    created = 0
    skipped = 0

    try:
        service = ProjectService(db)

        # Validate all parent experiences before making changes.
        resolved_experiences = {}

        for record in PROJECTS:
            key = (
                record["company"],
                record["designation"],
                record["experience_start_date"],
            )

            if key not in resolved_experiences:
                experience = find_experience(db, *key)

                if experience is None:
                    raise RuntimeError(
                        "Required experience not found: "
                        f"{record['company']} — {record['designation']} "
                        f"({record['experience_start_date']})"
                    )

                resolved_experiences[key] = experience

        # Create missing projects. Existing projects remain unchanged.
        for record in PROJECTS:
            experience_key = (
                record["company"],
                record["designation"],
                record["experience_start_date"],
            )
            experience = resolved_experiences[experience_key]

            existing_projects = service.get_by_experience_id(experience.id)
            existing = next(
                (
                    project
                    for project in existing_projects
                    if project.title.casefold() == record["title"].casefold()
                ),
                None,
            )

            if existing is not None:
                print(f"Skipped: {record['title']}")
                skipped += 1
                continue

            payload = ProjectCreate(
                experience_id=experience.id,
                title=record["title"],
                description=record["description"],
                role=record["role"],
                technologies=record["technologies"],
                project_url=record["project_url"],
                repository_url=record["repository_url"],
                start_date=record["start_date"],
                end_date=record["end_date"],
                display_order=record["display_order"],
            )

            service.create(payload)
            print(f"Created: {record['title']}")
            created += 1

        # Commit the complete seed operation as one transaction.
        db.commit()

        print()
        print("=" * 60)
        print("Project Seed Summary")
        print("=" * 60)
        print(f"Created: {created}")
        print(f"Skipped: {skipped}")
        print(f"Projects in seed dataset: {len(PROJECTS)}")
        print("Project seeding completed.")

    except Exception as exc:
        db.rollback()
        print()
        print("Project seed failed.")
        print(f"{type(exc).__name__}: {exc}")
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
