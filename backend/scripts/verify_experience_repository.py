"""
Verify ExperienceRepository operations.

Covers:

- Model import
- Repository import and initialization
- Repository model binding
- Experience CRUD
- Ordered experience retrieval
- Experience queries
- Skill queries
- Skill association management
- Duplicate skill handling
- Persistence
- Cascade deletion
- Final cleanup
"""

import sys
from datetime import date

from app.db.session import SessionLocal
from app.models import (
    Experience,
    Skill,
    experience_skills,
)
from app.repositories import ExperienceRepository
from app.schemas import ExperienceCreate
from sqlalchemy import select

def main() -> None:
    """
    Verify ExperienceRepository behaviour.
    """

    print("=" * 60)
    print("Experience Repository Verification")
    print("=" * 60)
    print()

    db = SessionLocal()

    repository = None

    experience_ids: list[int] = []
    skill_ids: list[int] = []

    try:

        # =========================================================
        # 1. Model Import
        # =========================================================

        assert Experience is not None
        assert Experience.__tablename__ == "experiences"

        print("✓ Experience model imports")

        # =========================================================
        # 2. Repository Import
        # =========================================================

        assert ExperienceRepository is not None

        print("✓ ExperienceRepository imports")

        # =========================================================
        # 3. Repository Initialization
        # =========================================================

        repository = ExperienceRepository(db)

        assert repository is not None

        print("✓ ExperienceRepository initializes")

        # =========================================================
        # 4. Repository Model Binding
        # =========================================================

        assert repository.model is Experience
        assert repository.db is db

        print("✓ Repository is bound to Experience")

        # =========================================================
        # Experience CRUD
        # =========================================================

        print()
        print("--- Experience CRUD ---")

        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        experience = repository.create(
            ExperienceCreate(
                company="Repository Test Company",
                designation="Software Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Hybrid",
                start_date=date(2020, 1, 1),
                end_date=date(2022, 12, 31),
                is_current=False,
                description=(
                    "Repository CRUD verification record."
                ),
                display_order=999,
            )
        )

        assert experience is not None
        assert experience.id is not None
        assert experience.company == "Repository Test Company"
        assert experience.designation == "Software Engineer"

        experience_ids.append(experience.id)

        print("✓ create() works")

        # ---------------------------------------------------------
        # Ordered get_all()
        # ---------------------------------------------------------

        ordering_experience_1 = repository.create(
            ExperienceCreate(
                company="Ordering Test 1",
                designation="Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Hybrid",
                start_date=date(2020, 1, 1),
                end_date=date(2021, 1, 1),
                is_current=False,
                description="Ordering test.",
                display_order=30,
            )
        )

        ordering_experience_2 = repository.create(
            ExperienceCreate(
                company="Ordering Test 2",
                designation="Senior Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Remote",
                start_date=date(2021, 1, 1),
                end_date=date(2022, 1, 1),
                is_current=False,
                description="Ordering test.",
                display_order=10,
            )
        )

        ordering_experience_3 = repository.create(
            ExperienceCreate(
                company="Ordering Test 3",
                designation="Lead Engineer",
                employment_type="Full-time",
                location="Coimbatore",
                location_type="Onsite",
                start_date=date(2022, 1, 1),
                end_date=None,
                is_current=True,
                description="Ordering test.",
                display_order=20,
            )
        )

        experience_ids.extend(
            [
                ordering_experience_1.id,
                ordering_experience_2.id,
                ordering_experience_3.id,
            ]
        )

        experiences = repository.get_all()

        orders = [
            item.display_order
            for item in experiences
        ]

        assert orders == sorted(orders)

        print("✓ get_all() ordered by display_order")

        # ---------------------------------------------------------
        # Get by ID
        # ---------------------------------------------------------

        fetched = repository.get_by_id(
            experience.id
        )

        assert fetched is not None
        assert fetched.id == experience.id
        assert fetched.company == "Repository Test Company"

        print("✓ get_by_id() works")

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        fetched.company = "Updated Repository Company"
        fetched.designation = "Senior Software Engineer"
        fetched.description = (
            "Updated repository verification record."
        )

        updated = repository.update(fetched)

        assert updated is not None
        assert updated.id == experience.id
        assert updated.company == "Updated Repository Company"
        assert updated.designation == "Senior Software Engineer"

        # ---------------------------------------------------------
        # CRUD Persistence
        # ---------------------------------------------------------

        persisted = repository.get_by_id(
            experience.id
        )

        assert persisted is not None
        assert persisted.company == (
            "Updated Repository Company"
        )
        assert persisted.designation == (
            "Senior Software Engineer"
        )
        assert persisted.description == (
            "Updated repository verification record."
        )

        print("✓ CRUD persists correctly")

        # =========================================================
        # Experience Queries
        # =========================================================

        print()
        print("--- Experience Queries ---")

        # ---------------------------------------------------------
        # get_current()
        # ---------------------------------------------------------

        current_experience = repository.create(
            ExperienceCreate(
                company="Current Test Company",
                designation="Lead Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Remote",
                start_date=date(2024, 1, 1),
                end_date=None,
                is_current=True,
                description=(
                    "Current experience query test."
                ),
                display_order=5,
            )
        )

        experience_ids.append(current_experience.id)

        current = repository.get_current()

        assert current
        assert all(
            item.is_current
            for item in current
        )

        assert any(
            item.id == current_experience.id
            and item.display_order == 5
            for item in current
        )

        print("✓ get_current() works")

        # ---------------------------------------------------------
        # get_by_company()
        # ---------------------------------------------------------

        company_results = repository.get_by_company(
            "Current Test Company"
        )

        assert company_results

        assert all(
            item.company == "Current Test Company"
            for item in company_results
        )

        print("✓ get_by_company() works")

        # ---------------------------------------------------------
        # Case-insensitive company
        # ---------------------------------------------------------

        company_results = repository.get_by_company(
            "current test company"
        )

        assert company_results

        assert all(
            item.company == "Current Test Company"
            for item in company_results
        )

        print("✓ get_by_company() is case-insensitive")

        # ---------------------------------------------------------
        # get_by_employment_type()
        # ---------------------------------------------------------

        employment_results = (
            repository.get_by_employment_type(
                "full-time"
            )
        )

        assert employment_results

        assert all(
            item.employment_type.lower()
            == "full-time"
            for item in employment_results
        )

        print("✓ get_by_employment_type() works")

        # ---------------------------------------------------------
        # get_by_location_type()
        # ---------------------------------------------------------

        location_results = (
            repository.get_by_location_type(
                "remote"
            )
        )

        assert location_results

        assert all(
            item.location_type.lower()
            == "remote"
            for item in location_results
        )

        print("✓ get_by_location_type() works")

        # =========================================================
        # Test Skills
        # =========================================================

        print()
        print("--- Skill Queries ---")

        # ---------------------------------------------------------
        # Create test skills
        #
        # These fields match the current Skill model used by the
        # portfolio project.
        # ---------------------------------------------------------

        skill_python = Skill(
            name="Repository Test Python",
            category="Programming & Software Development",
            proficiency=90,
            display_order=900,
        )

        skill_fastapi = Skill(
            name="Repository Test FastAPI",
            category="Backend Development",
            proficiency=85,
            display_order=901,
        )

        skill_aws = Skill(
            name="Repository Test AWS",
            category="Cloud & DevOps",
            proficiency=80,
            display_order=902,
        )

        db.add_all(
            [
                skill_python,
                skill_fastapi,
                skill_aws,
            ]
        )

        db.commit()

        db.refresh(skill_python)
        db.refresh(skill_fastapi)
        db.refresh(skill_aws)

        skill_ids.extend(
            [
                skill_python.id,
                skill_fastapi.id,
                skill_aws.id,
            ]
        )

        # ---------------------------------------------------------
        # Create dedicated skill-query experience
        # ---------------------------------------------------------

        skill_experience_1 = repository.create(
            ExperienceCreate(
                company="Skill Query Company A",
                designation="Python Engineer",
                employment_type="Full-time",
                location="Hyderabad",
                location_type="Remote",
                start_date=date(2022, 1, 1),
                end_date=date(2023, 1, 1),
                is_current=False,
                description="Skill query test A.",
                display_order=100,
            )
        )

        skill_experience_2 = repository.create(
            ExperienceCreate(
                company="Skill Query Company B",
                designation="Backend Engineer",
                employment_type="Full-time",
                location="Bangalore",
                location_type="Hybrid",
                start_date=date(2023, 1, 1),
                end_date=None,
                is_current=True,
                description="Skill query test B.",
                display_order=110,
            )
        )

        experience_ids.extend(
            [
                skill_experience_1.id,
                skill_experience_2.id,
            ]
        )

        # =========================================================
        # Skill Queries
        # =========================================================

        # ---------------------------------------------------------
        # get_by_skill_id()
        # ---------------------------------------------------------

        repository.add_skill(
            skill_experience_1.id,
            skill_python.id,
        )

        repository.add_skill(
            skill_experience_2.id,
            skill_python.id,
        )

        db.commit()

        experiences_by_skill_id = (
            repository.get_by_skill_id(
                skill_python.id
            )
        )

        result_ids = [
            item.id
            for item in experiences_by_skill_id
        ]

        assert skill_experience_1.id in result_ids
        assert skill_experience_2.id in result_ids

        assert result_ids == sorted(
            result_ids,
            key=lambda item_id: repository.get_by_id(
                item_id
            ).display_order
        )

        print("✓ get_by_skill_id() works")

        # ---------------------------------------------------------
        # get_by_skill_name()
        # ---------------------------------------------------------

        experiences_by_skill_name = (
            repository.get_by_skill_name(
                "repository test python"
            )
        )

        result_ids = [
            item.id
            for item in experiences_by_skill_name
        ]

        assert skill_experience_1.id in result_ids
        assert skill_experience_2.id in result_ids

        print("✓ get_by_skill_name() works")

        # ---------------------------------------------------------
        # get_skill_ids()
        # ---------------------------------------------------------

        skill_ids_for_experience = (
            repository.get_skill_ids(
                skill_experience_1.id
            )
        )

        assert skill_python.id in skill_ids_for_experience

        print("✓ get_skill_ids() works")

        # =========================================================
        # Skill Management
        # =========================================================

        print()
        print("--- Skill Management ---")

        # ---------------------------------------------------------
        # add_skill()
        # ---------------------------------------------------------

        repository.add_skill(
            skill_experience_1.id,
            skill_fastapi.id,
        )

        current_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert skill_fastapi.id in current_skill_ids

        print("✓ add_skill() works")

        # ---------------------------------------------------------
        # duplicate add_skill()
        # ---------------------------------------------------------

        repository.add_skill(
            skill_experience_1.id,
            skill_fastapi.id,
        )

        db.commit()

        current_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert current_skill_ids.count(
            skill_fastapi.id
        ) == 1

        print("✓ duplicate add_skill() is ignored")

        # ---------------------------------------------------------
        # remove_skill()
        # ---------------------------------------------------------

        repository.remove_skill(
            skill_experience_1.id,
            skill_fastapi.id,
        )

        db.commit()

        current_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert skill_fastapi.id not in current_skill_ids

        print("✓ remove_skill() works")

        # ---------------------------------------------------------
        # set_skills()
        # ---------------------------------------------------------

        repository.set_skills(
            skill_experience_1.id,
            [
                skill_python.id,
                skill_fastapi.id,
                skill_aws.id,
            ],
        )

        db.commit()

        current_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert set(current_skill_ids) == {
            skill_python.id,
            skill_fastapi.id,
            skill_aws.id,
        }

        print("✓ set_skills() works")

        # ---------------------------------------------------------
        # Duplicate handling in set_skills()
        # ---------------------------------------------------------

        repository.set_skills(
            skill_experience_1.id,
            [
                skill_python.id,
                skill_python.id,
                skill_fastapi.id,
                skill_fastapi.id,
                skill_aws.id,
                skill_aws.id,
            ],
        )

        db.commit()

        current_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert len(current_skill_ids) == 3
        assert len(set(current_skill_ids)) == 3

        assert set(current_skill_ids) == {
            skill_python.id,
            skill_fastapi.id,
            skill_aws.id,
        }

        print(
            "✓ duplicate skill IDs are removed by set_skills()"
        )

        # ---------------------------------------------------------
        # clear_skills()
        # ---------------------------------------------------------

        repository.clear_skills(
            skill_experience_1.id
        )

        db.commit()

        current_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert current_skill_ids == []

        print("✓ clear_skills() works")

        # =========================================================
        # Persistence
        # =========================================================

        print()
        print("--- Persistence ---")

        # ---------------------------------------------------------
        # Restore associations for persistence test
        # ---------------------------------------------------------

        repository.set_skills(
            skill_experience_1.id,
            [
                skill_python.id,
                skill_fastapi.id,
            ],
        )

        db.commit()

        # Expire ORM state and query database again.
        db.expire_all()

        persisted_skill_ids = repository.get_skill_ids(
            skill_experience_1.id
        )

        assert set(persisted_skill_ids) == {
            skill_python.id,
            skill_fastapi.id,
        }

        print("✓ skill association persistence")

        # ---------------------------------------------------------
        # CRUD persistence
        # ---------------------------------------------------------

        persisted_experience = repository.get_by_id(
            experience.id
        )

        assert persisted_experience is not None
        assert (
            persisted_experience.company
            == "Updated Repository Company"
        )
        assert (
            persisted_experience.designation
            == "Senior Software Engineer"
        )

        print("✓ CRUD persistence")

        # =========================================================
        # Delete & Cascade
        # =========================================================

        print()
        print("--- Delete & Cascade ---")

        # ---------------------------------------------------------
        # Capture association count before deletion
        # ---------------------------------------------------------

        association_statement = (
            select(experience_skills)
            .where(
                experience_skills.c.experience_id
                == skill_experience_1.id
            )
        )

        associations_before_delete = list(
            db.execute(
                association_statement
            ).all()
        )

        assert associations_before_delete

        # ---------------------------------------------------------
        # Delete experience
        # ---------------------------------------------------------

        repository.delete(
            skill_experience_1
        )

        print("✓ delete() works")

        # ---------------------------------------------------------
        # Experience should no longer exist
        # ---------------------------------------------------------

        deleted = repository.get_by_id(
            skill_experience_1.id
        )

        assert deleted is None

        print(
            "✓ Deleted experience is no longer retrievable"
        )

        # ---------------------------------------------------------
        # Verify experience_skill cascade
        # ---------------------------------------------------------

        remaining_associations = list(
            db.execute(
                association_statement
            ).all()
        )

        assert remaining_associations == []

        print(
            "✓ experience_skill associations cascade "
            "on experience deletion"
        )

        # ---------------------------------------------------------
        # Skills must remain
        # ---------------------------------------------------------

        remaining_skill_1 = db.get(
            Skill,
            skill_python.id,
        )

        remaining_skill_2 = db.get(
            Skill,
            skill_fastapi.id,
        )

        remaining_skill_3 = db.get(
            Skill,
            skill_aws.id,
        )

        assert remaining_skill_1 is not None
        assert remaining_skill_2 is not None
        assert remaining_skill_3 is not None

        print("✓ Skills remain after experience deletion")

        # =========================================================
        # Cleanup
        # =========================================================

        print()
        print("--- Cleanup ---")

        # ---------------------------------------------------------
        # Delete remaining test experiences
        # ---------------------------------------------------------

        for test_experience_id in experience_ids:

            # The cascade-tested experience has already been deleted.
            if test_experience_id == skill_experience_1.id:
                continue

            test_experience = repository.get_by_id(
                test_experience_id
            )

            if test_experience is not None:
                repository.delete(
                    test_experience
                )

        # ---------------------------------------------------------
        # Delete test skills
        # ---------------------------------------------------------

        for test_skill_id in skill_ids:

            test_skill = db.get(
                Skill,
                test_skill_id,
            )

            if test_skill is not None:
                db.delete(test_skill)

        db.commit()

        # ---------------------------------------------------------
        # Verify cleanup
        # ---------------------------------------------------------

        for test_experience_id in experience_ids:

            assert repository.get_by_id(
                test_experience_id
            ) is None

        for test_skill_id in skill_ids:

            assert db.get(
                Skill,
                test_skill_id,
            ) is None

        print("✓ final cleanup")

        # =========================================================
        # Summary
        # =========================================================

        print()
        print("=" * 60)
        print("Repository Verification Summary")
        print("=" * 60)

        print("✓ Repository initialization")
        print("✓ Model binding")
        print("✓ CRUD operations")
        print("✓ Ordered get_all()")
        print("✓ Experience queries")
        print("✓ Skill queries")
        print("✓ Skill management")
        print("✓ Persistence")
        print("✓ Cascade deletion")
        print("✓ Cleanup")

        print()
        print(
            "🎉 ExperienceRepository verified successfully."
        )

    except AssertionError as exc:

        print()
        print("❌ Repository verification failed")

        if exc:
            print(exc)

        # Roll back any uncommitted transaction.
        db.rollback()

        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)

        db.rollback()

        sys.exit(1)

    finally:

        # ---------------------------------------------------------
        # Final database cleanup attempt
        #
        # This is intentionally defensive. If verification fails
        # halfway through, remove only records created by this
        # verification run.
        # ---------------------------------------------------------

        try:

            db.rollback()

            if repository is not None:

                for test_experience_id in experience_ids:

                    test_experience = repository.get_by_id(
                        test_experience_id
                    )

                    if test_experience is not None:
                        repository.delete(
                            test_experience
                        )

            for test_skill_id in skill_ids:

                test_skill = db.get(
                    Skill,
                    test_skill_id,
                )

                if test_skill is not None:
                    db.delete(test_skill)

            db.commit()

        except Exception:
            db.rollback()

        finally:
            db.close()

    print("=" * 60)
    print("Repository verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()