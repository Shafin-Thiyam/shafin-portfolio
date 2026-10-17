
"""
Verify seeded experience data and skill associations.
"""

import sys
from datetime import date

from app.db.session import SessionLocal
from app.models import Skill
from app.repositories import ExperienceRepository
from scripts.seed_experience import main as seed_main
from sqlalchemy import select


# Expected experience records and their skill associations.
# Skill names are used instead of database IDs so that the
# verification remains stable across database environments.

EXPECTED_EXPERIENCES = [
    {
        "company": "Tata Consultancy Services (TCS)",
        "designation": "Associate Consultant",
        "start_date": date(2022, 9, 1),
        "end_date": None,
        "is_current": True,
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "display_order": 1,
        "skills": [
            "Python",
            "FastAPI",
            "REST APIs",
            "Prompt Engineering",
            "Generative AI",
            "LLM Fundamentals",
            "Model Context Protocol (MCP)",
            "AI Agents",
            "Langfuse",
            "SAP BTP",
            "SAP AI Core",
            "SAP Data Intelligence",
            "SAP BTP Cloud Foundry",
            "SAP Kyma",
            "AWS Lambda",
            "AWS S3",
            "Snowflake",
            "Kafka",
            "HANA DB",
            "HANA Data Lake",
            "AEM",
            "Git",
            "Docker",
            "Kubernetes",
            "UNIX",
            "CI/CD",
            "Technical Leadership",
            "POC & Feasibility Analysis",
            "Risk Assessment",
            "Peer Reviews",
            "Knowledge Transfer",
            "Internal Training",
            "Technical Interviews",
            "Cross-functional Collaboration",
        ],
    },
    {
        "company": "Thomson Reuters",
        "designation": "Associate Lead",
        "start_date": date(2021, 4, 1),
        "end_date": date(2022, 9, 30),
        "is_current": False,
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "Hybrid",
        "display_order": 2,
        "skills": [
            "Python",
            "XSL",
            "Agile/Scrum",
            "Risk Assessment",
            "Knowledge Transfer",
            "Cross-functional Collaboration",
        ],
    },
    {
        "company": "Thomson Reuters",
        "designation": "Senior Software Engineer",
        "start_date": date(2016, 6, 1),
        "end_date": date(2021, 3, 31),
        "is_current": False,
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "Hybrid",
        "display_order": 3,
        "skills": [
            "Python",
            "Flask",
            "REST APIs",
            "XSL",
            "XSLT",
            "XPath",
            "XML",
            "XSD",
            "DTD",
            "HTML",
            "JavaScript",
            "Web Scraping",
        ],
    },
    {
        "company": "Wipro Technologies",
        "designation": "Senior System Engineer",
        "start_date": date(2014, 12, 1),
        "end_date": date(2016, 6, 30),
        "is_current": False,
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "display_order": 4,
        "skills": ["XSL", "XML", "XSD"],
    },
    {
        "company": "Thomson Reuters",
        "designation": "Software Engineer",
        "start_date": date(2011, 6, 1),
        "end_date": date(2014, 11, 30),
        "is_current": False,
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "display_order": 5,
        "skills": ["XSL", "XML", "XSD", "JavaScript"],
    },
    {
        "company": "Infosys BPM",
        "designation": "Process Executive",
        "start_date": date(2010, 2, 1),
        "end_date": date(2011, 6, 30),
        "is_current": False,
        "employment_type": "Full-time",
        "location": "Pune, India",
        "location_type": "On-site",
        "display_order": 6,
        "skills": [
            "XSLT",
            "XML",
            "XSD",
            "DTD",
            "HTML",
            "CSS",
            "Perl",
            "UNIX",
        ],
    },
]


def experience_key(experience) -> tuple:
    """Return the natural key for an experience."""
    return (
        experience.company,
        experience.designation,
        experience.start_date,
    )


def get_skill_id_map(db) -> dict[str, int]:
    """Return skill names mapped to their database IDs."""
    skills = db.scalars(select(Skill)).all()
    return {skill.name: skill.id for skill in skills}


def get_association_snapshot(repository, experiences) -> dict:
    """Capture skill associations for the expected experiences."""
    snapshot = {}

    for expected in EXPECTED_EXPERIENCES:
        matches = [
            experience
            for experience in experiences
            if experience_key(experience)
            == (
                expected["company"],
                expected["designation"],
                expected["start_date"],
            )
        ]

        assert len(matches) == 1, (
            "Cannot snapshot associations: expected exactly one "
            f"record for {expected['company']} — "
            f"{expected['designation']}, found {len(matches)}."
        )

        experience = matches[0]
        snapshot[experience_key(experience)] = tuple(
            sorted(repository.get_skill_ids(experience.id))
        )

    return snapshot


def main() -> None:
    """Verify seeded experience data."""
    print("=" * 60)
    print("Experience Seed Verification")
    print("=" * 60)

    db = SessionLocal()

    try:
        repository = ExperienceRepository(db)

        # ---------------------------------------------------------
        # Database Connection
        # ---------------------------------------------------------

        db.execute(select(1)).scalar_one()
        print("✓ Database connected")

        # ---------------------------------------------------------
        # Required Skills
        # ---------------------------------------------------------

        skill_id_map = get_skill_id_map(db)

        expected_skill_names = {
            skill_name
            for experience in EXPECTED_EXPERIENCES
            for skill_name in experience["skills"]
        }

        missing_skills = expected_skill_names - set(skill_id_map)

        assert not missing_skills, (
            "Required skills are missing: "
            + ", ".join(sorted(missing_skills))
        )

        print("✓ All required skills exist")

        # ---------------------------------------------------------
        # Experience Records
        # ---------------------------------------------------------

        experiences = repository.get_all()

        for expected in EXPECTED_EXPERIENCES:
            matching = [
                item
                for item in experiences
                if experience_key(item)
                == (
                    expected["company"],
                    expected["designation"],
                    expected["start_date"],
                )
            ]

            assert len(matching) == 1, (
                f"Expected exactly one experience for "
                f"{expected['company']} — {expected['designation']}; "
                f"found {len(matching)}."
            )

            experience = matching[0]

            for field in (
                "company",
                "designation",
                "start_date",
                "end_date",
                "is_current",
                "employment_type",
                "location",
                "location_type",
                "display_order",
            ):
                actual = getattr(experience, field)
                expected_value = expected[field]

                assert actual == expected_value, (
                    f"{expected['company']} — {expected['designation']}: "
                    f"{field} expected {expected_value!r}, "
                    f"got {actual!r}."
                )

            assert experience.description, (
                f"Description is missing for "
                f"{expected['company']} — {expected['designation']}."
            )

        print("✓ All six experience records and key fields verified")

        # ---------------------------------------------------------
        # Current Employment
        # ---------------------------------------------------------

        current_experiences = [
            item for item in experiences if item.is_current
        ]

        assert len(current_experiences) == 1, (
            "Expected exactly one current experience; "
            f"found {len(current_experiences)}."
        )

        current = current_experiences[0]

        assert current.company == "Tata Consultancy Services (TCS)"
        assert current.end_date is None

        print("✓ Current employment and dates verified")

        # ---------------------------------------------------------
        # Display Order
        # ---------------------------------------------------------

        expected_orders = [
            item["display_order"]
            for item in EXPECTED_EXPERIENCES
        ]

        actual_orders = [
            next(
                experience.display_order
                for experience in experiences
                if experience_key(experience)
                == (
                    expected["company"],
                    expected["designation"],
                    expected["start_date"],
                )
            )
            for expected in EXPECTED_EXPERIENCES
        ]

        assert actual_orders == expected_orders, (
            f"Expected display order {expected_orders}; "
            f"got {actual_orders}."
        )

        print("✓ Display order verified")

        # ---------------------------------------------------------
        # Duplicate Prevention
        # ---------------------------------------------------------

        keys = [experience_key(item) for item in experiences]

        for expected in EXPECTED_EXPERIENCES:
            key = (
                expected["company"],
                expected["designation"],
                expected["start_date"],
            )
            assert keys.count(key) == 1, (
                f"Duplicate experience detected for {key}."
            )

        print("✓ Duplicate prevention verified")

        # ---------------------------------------------------------
        # Skill Associations
        # ---------------------------------------------------------

        association_snapshot = get_association_snapshot(
            repository, experiences
        )

        for expected in EXPECTED_EXPERIENCES:
            key = (
                expected["company"],
                expected["designation"],
                expected["start_date"],
            )

            experience = next(
                item for item in experiences
                if experience_key(item) == key
            )

            actual_skill_ids = set(
                repository.get_skill_ids(experience.id)
            )

            expected_skill_ids = {
                skill_id_map[name] for name in expected["skills"]
            }

            assert actual_skill_ids == expected_skill_ids, (
                f"Skill associations mismatch for "
                f"{expected['company']} — {expected['designation']}. "
                f"Missing IDs: "
                f"{sorted(expected_skill_ids - actual_skill_ids)}. "
                f"Unexpected IDs: "
                f"{sorted(actual_skill_ids - expected_skill_ids)}."
            )

        print("✓ All six skill association sets verified")

        # ---------------------------------------------------------
        # Required Fields
        # ---------------------------------------------------------

        for expected in EXPECTED_EXPERIENCES:
            experience = next(
                item for item in experiences
                if experience_key(item)
                == (
                    expected["company"],
                    expected["designation"],
                    expected["start_date"],
                )
            )

            assert experience.company
            assert experience.designation
            assert experience.employment_type
            assert experience.location
            assert experience.location_type
            assert experience.start_date
            assert experience.description
            assert experience.display_order >= 1

        print("✓ Required fields verified")

        # ---------------------------------------------------------
        # Seed Idempotency
        # ---------------------------------------------------------

        count_before = len(repository.get_all())
        associations_before = get_association_snapshot(
            repository, repository.get_all()
        )

        print()
        print("Running experience seed again to verify idempotency...")
        seed_main()

        # The seed uses its own database session. Expire this session's
        # cached ORM state before verifying the persisted result.
        db.expire_all()

        experiences_after = repository.get_all()
        count_after = len(experiences_after)

        assert count_before == count_after, (
            f"Experience count changed from {count_before} "
            f"to {count_after} after reseeding."
        )

        associations_after = get_association_snapshot(
            repository, experiences_after
        )

        assert associations_before == associations_after, (
            "Skill associations changed after reseeding."
        )

        print("✓ Seed idempotency verified")
        print("✓ Skill associations unchanged after reseeding")

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        print()
        print("=" * 60)
        print("Experience Seed Verification Summary")
        print("=" * 60)
        print("✓ Database connection")
        print("✓ Required skills")
        print("✓ Six seeded experience records")
        print("✓ Employment fields and dates")
        print("✓ Current employment")
        print("✓ Display order")
        print("✓ Duplicate prevention")
        print("✓ Skill associations")
        print("✓ Required fields")
        print("✓ Seed idempotency")
        print()
        print("🎉 Experience seed verified successfully.")

    except AssertionError as exc:
        print()
        print("❌ Experience seed verification failed")
        print(exc)
        db.rollback()
        sys.exit(1)

    except SystemExit:
        # The seed script may call sys.exit() when it encounters an error.
        db.rollback()
        raise

    except Exception as exc:
        print()
        print("❌ Unexpected error")
        print(f"{type(exc).__name__}: {exc}")
        db.rollback()
        sys.exit(1)

    finally:
        db.close()

    print("=" * 60)
    print("Experience seed verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
