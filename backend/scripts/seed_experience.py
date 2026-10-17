
"""
Seed portfolio experience data and skill associations.

Run from the backend directory:
    python -m scripts.seed_experience
"""

import sys
from datetime import date

from app.db.session import SessionLocal
from app.schemas import ExperienceCreate
from app.services import ExperienceService, SkillService


EXPERIENCES = [
    {
        "company": "Tata Consultancy Services (TCS)",
        "designation": "Associate Consultant",
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "start_date": "2022-09-01",
        "end_date": None,
        "is_current": True,
        "description": (
            "Client: Apple. Developed AI agents and tools using "
            "Langfuse and explored agentic AI patterns for enterprise "
            "GenAI use cases within SAP BTP. Led the migration of SAP "
            "Data Intelligence applications to SAP AI Core, successfully "
            "migrating three applications from POC through production. "
            "Implemented AI lifecycle management practices for tracking, "
            "deploying, and managing ML artifacts. Engineered secure SAP "
            "BTP audit and usage log integration with Kafka through AEM. "
            "Developed Python-based POCs, feasibility assessments, REST "
            "API integrations, and automation solutions using AWS Lambda, "
            "AWS S3, HANA Data Lake, HANA DB, Docker, and Kubernetes. "
            "Developed SAP Data Intelligence pipelines and conducted "
            "technical risk assessments, peer reviews, knowledge-transfer "
            "sessions, and internal technical training."
        ),
        "display_order": 1,
    },
    {
        "company": "Thomson Reuters",
        "designation": "Associate Lead",
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "start_date": "2021-04-01",
        "end_date": "2022-09-30",
        "is_current": False,
        "description": (
            "Led integration activities for migration from legacy "
            "processes to next-generation processes, supporting technical "
            "transition and operational continuity. Coordinated "
            "knowledge-transfer sessions for new hires and junior team "
            "members. Automated manual tasks and business workflows using "
            "Microsoft Power Automate and supported the Checkpoint "
            "content-delivery platform. Technologies included Python, "
            "XSL, and Microsoft Power Automate."
        ),
        "display_order": 2,
    },
    {
        "company": "Thomson Reuters",
        "designation": "Senior Software Engineer",
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "start_date": "2016-06-01",
        "end_date": "2021-03-31",
        "is_current": False,
        "description": (
            "Engineered content-processing and publishing pipelines to "
            "generate publication-ready books and transform legacy GAAP "
            "content into new business-logic schemas. Developed end-to-end "
            "content transformation workflows involving HTML web scraping, "
            "XML transformation using XSLT, XSD schema creation and "
            "validation, and conversion of validated XML back to HTML. "
            "Developed a Flask REST API to accept XML input, execute "
            "specified stylesheets, and return transformed XML output in "
            "JSON format. Technologies included Python, Flask, XSL/XSLT, "
            "XSD, XML, DTD, HTML, and REST APIs."
        ),
        "display_order": 3,
    },
    {
        "company": "Wipro Technologies",
        "designation": "Senior System Engineer",
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "start_date": "2014-12-01",
        "end_date": "2016-06-30",
        "is_current": False,
        "description": (
            "Client: RR Donnelly. Engineered document-comparison "
            "transformations using XSL 2.0 filters to merge and process "
            "old and new document versions. Validated transformation "
            "changes and supported testing activities in the pagePro "
            "publishing environment. Technologies included XSL 2.0, "
            "XSD, and XML."
        ),
        "display_order": 4,
    },
    {
        "company": "Thomson Reuters",
        "designation": "Software Engineer",
        "employment_type": "Full-time",
        "location": "Hyderabad, India",
        "location_type": "On-site",
        "start_date": "2011-06-01",
        "end_date": "2014-11-30",
        "is_current": False,
        "description": (
            "Migrated XSL 1.0 stylesheets to XSL 2.0 and resolved "
            "stylesheet transformation issues across publishing workflows. "
            "Debugged XML, XSD, and XSL transformation issues to maintain "
            "reliable content-processing pipelines. Technologies included "
            "JavaScript, XSL 2.0, XSD, and XML."
        ),
        "display_order": 5,
    },
    {
        "company": "Infosys BPM",
        "designation": "Process Executive",
        "employment_type": "Full-time",
        "location": "Pune, India",
        "location_type": "On-site",
        "start_date": "2010-02-01",
        "end_date": "2011-06-30",
        "is_current": False,
        "description": (
            "Client: LexisNexis. Analyzed schema mappings and developed "
            "and tested XSLT stylesheets for XML transformation workflows. "
            "Validated transformed XML against XML schemas, documented "
            "schema-related defects, generated test cases, and executed "
            "final stylesheets in UNIX environments to support production "
            "publishing workflows. Technologies included XML, XSLT, "
            "HTML, CSS, Perl, and UNIX."
        ),
        "display_order": 6,
    },
]


# Skill names are used instead of database IDs so this seed works
# even when IDs differ between database environments.
EXPERIENCE_SKILLS = {
    ("Tata Consultancy Services (TCS)", "Associate Consultant", "2022-09-01"): [
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
    ("Thomson Reuters", "Associate Lead", "2021-04-01"): [
        "Python",
        "XSL",
        "Agile/Scrum",
        "Risk Assessment",
        "Knowledge Transfer",
        "Cross-functional Collaboration",
    ],
    ("Thomson Reuters", "Senior Software Engineer", "2016-06-01"): [
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
    ("Wipro Technologies", "Senior System Engineer", "2014-12-01"): [
        "XSL",
        "XML",
        "XSD",
    ],
    ("Thomson Reuters", "Software Engineer", "2011-06-01"): [
        "XSL",
        "XML",
        "XSD",
        "JavaScript",
    ],
    ("Infosys BPM", "Process Executive", "2010-02-01"): [
        "XSLT",
        "XML",
        "XSD",
        "DTD",
        "HTML",
        "CSS",
        "Perl",
        "UNIX",
    ],
}


def experience_key(
    company: str,
    designation: str,
    start_date: str,
) -> tuple[str, str, str]:
    """Build the natural key used to identify an experience."""

    return company, designation, start_date


def find_existing_experience(
    service: ExperienceService,
    payload: ExperienceCreate,
):
    """Find an experience by company, designation, and start date."""

    for existing in service.get_by_company(payload.company):
        if (
            existing.designation.casefold()
            == payload.designation.casefold()
            and existing.start_date == payload.start_date
        ):
            return existing

    return None


def main() -> None:
    """Seed experiences and reconcile their skill associations."""

    print("=" * 60)
    print("Experience Seed")
    print("=" * 60)

    db = SessionLocal()

    created = 0
    skipped = 0
    associations_reconciled = 0

    try:
        experience_service = ExperienceService(db)
        skill_service = SkillService(db)

        # Validate every required skill before changing experience data.
        required_skill_names = {
            skill_name
            for names in EXPERIENCE_SKILLS.values()
            for skill_name in names
        }

        skills_by_name = {}

        for skill_name in sorted(required_skill_names):
            skill = skill_service.get_skill_by_name(skill_name)

            if skill is None:
                missing = [
                    name
                    for name in sorted(required_skill_names)
                    if skill_service.get_skill_by_name(name) is None
                ]
                raise RuntimeError(
                    "Required skills are missing from the database: "
                    + ", ".join(missing)
                )

            skills_by_name[skill_name] = skill

        # Create missing experience records; leave existing records intact.
        for record in EXPERIENCES:
            payload = ExperienceCreate(
                **{
                    **record,
                    "start_date": date.fromisoformat(
                        record["start_date"]
                    ),
                    "end_date": (
                        date.fromisoformat(record["end_date"])
                        if record["end_date"]
                        else None
                    ),
                }
            )

            existing = find_existing_experience(
                experience_service,
                payload,
            )

            if existing is None:
                existing = experience_service.create(payload)
                print(
                    f"Created experience: "
                    f"{payload.company} — {payload.designation}"
                )
                created += 1
            else:
                print(
                    f"Skipped experience: "
                    f"{payload.company} — {payload.designation}"
                )
                skipped += 1

            key = experience_key(
                payload.company,
                payload.designation,
                payload.start_date.isoformat(),
            )

            skill_names = EXPERIENCE_SKILLS[key]
            skill_ids = [
                skills_by_name[name].id
                for name in skill_names
            ]

            current_skill_ids = set(
                experience_service.get_skill_ids(existing.id)
            )
            desired_skill_ids = set(skill_ids)

            if current_skill_ids != desired_skill_ids:
                experience_service.set_skills(
                    existing.id,
                    skill_ids,
                )
                associations_reconciled += 1
                print(
                    f"  Reconciled skills: {len(skill_ids)} "
                    f"desired associations"
                )
            else:
                print("  Skill associations already match.")

        print()
        print("=" * 60)
        print("Experience Seed Summary")
        print("=" * 60)
        print(f"Experiences created             : {created}")
        print(f"Experiences skipped             : {skipped}")
        print(f"Association sets reconciled     : {associations_reconciled}")
        print(f"Experiences in seed dataset     : {len(EXPERIENCES)}")
        print("Experience seeding completed.")

    except Exception as exc:
        db.rollback()
        print()
        print("Experience seed failed.")
        print(f"{type(exc).__name__}: {exc}")
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
