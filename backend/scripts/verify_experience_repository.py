"""
Verify ExperienceRepository base CRUD operations.
"""

import sys
from datetime import date

from app.db.session import SessionLocal
from app.models import Experience
from app.repositories import ExperienceRepository
from app.schemas import ExperienceCreate


def main() -> None:
    """
    Verify ExperienceRepository base CRUD operations.
    """

    print("=" * 60)
    print("Experience Repository Verification")
    print("=" * 60)

    db = SessionLocal()

    experience_id = None

    try:

        # ---------------------------------------------------------
        # 1. Verify Experience Model Import
        # ---------------------------------------------------------

        assert Experience is not None
        assert Experience.__tablename__ == "experiences"

        print("✓ Experience model imports")

        # ---------------------------------------------------------
        # 2. Verify Repository Import
        # ---------------------------------------------------------

        assert ExperienceRepository is not None

        print("✓ ExperienceRepository imports")

        # ---------------------------------------------------------
        # 3. Repository Initialization
        # ---------------------------------------------------------

        repository = ExperienceRepository(db)

        assert repository is not None

        print("✓ ExperienceRepository initializes")

        # ---------------------------------------------------------
        # 4. Repository Model Binding
        # ---------------------------------------------------------

        assert repository.model is Experience
        assert repository.db is db

        print("✓ Repository is bound to Experience")

        # ---------------------------------------------------------
        # 5. Create
        # ---------------------------------------------------------

        create_data = ExperienceCreate(
            company="Repository Test Company",
            designation="Software Engineer",
            employment_type="Full-time",
            location="Hyderabad",
            location_type="Hybrid",
            start_date=date(2020, 1, 1),
            end_date=date(2022, 12, 31),
            is_current=False,
            description="Repository CRUD verification record.",
            display_order=999,
        )

        experience = repository.create(create_data)

        assert experience is not None
        assert experience.id is not None
        assert experience.company == "Repository Test Company"
        assert experience.designation == "Software Engineer"

        experience_id = experience.id

        print("✓ create() works")
        
        # ---------------------------------------------------------
        # 6. order verification
        # ---------------------------------------------------------
        experience_1 = repository.create(
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

        experience_2 = repository.create(
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

        experience_3 = repository.create(
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
        experiences = repository.get_all()

        orders = [
            experience.display_order
            for experience in experiences
        ]
        assert orders == sorted(orders)
        print("✓ get_all() ordered by display_order")
        
        # ---------------------------------------------------------
        # 7. Get by ID
        # ---------------------------------------------------------

        fetched = repository.get_by_id(experience_id)

        assert fetched is not None
        assert fetched.id == experience_id
        assert fetched.company == "Repository Test Company"

        print("✓ get_by_id() works")

        # ---------------------------------------------------------
        # 8. Update
        # ---------------------------------------------------------

        fetched.company = "Updated Repository Company"
        fetched.designation = "Senior Software Engineer"
        fetched.description = "Updated repository verification record."

        updated = repository.update(fetched)

        assert updated is not None
        assert updated.id == experience_id
        assert updated.company == "Updated Repository Company"
        assert updated.designation == "Senior Software Engineer"

        print("✓ update() works")

        # ---------------------------------------------------------
        # 9. Verify Updated Data Persists
        # ---------------------------------------------------------

        persisted = repository.get_by_id(experience_id)

        assert persisted is not None
        assert persisted.company == "Updated Repository Company"
        assert persisted.designation == "Senior Software Engineer"
        assert (
            persisted.description
            == "Updated repository verification record."
        )

        print("✓ CRUD persists correctly")
        
        # --------------------------------------------------------------------------------------
        # 10. Get Current, get by Company, get by employment type, get by location type records
        # --------------------------------------------------------------------------------------
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
                description="Current experience query test.",
                display_order=5,
            )
        )
        current = repository.get_current()

        assert current

        assert all(
            experience.is_current
            for experience in current
        )

        assert current[0].display_order == 5

        print("✓ get_current() works")
        
        
        company_results = repository.get_by_company(
            "Current Test Company"
        )

        assert company_results

        assert all(
            experience.company == "Current Test Company"
            for experience in company_results
        )

        print("✓ get_by_company() works")
        
        company_results = repository.get_by_company(
            "current test company"
        )

        assert company_results

        print("✓ get_by_company() is case-insensitive")
        
        employment_results = (
            repository.get_by_employment_type(
                "full-time"
            )
        )

        assert employment_results

        assert all(
            experience.employment_type.lower()
            == "full-time"
            for experience in employment_results
        )

        print("✓ get_by_employment_type() works")
        
        location_results = (
            repository.get_by_location_type(
                "remote"
            )
        )

        assert location_results

        assert all(
            experience.location_type.lower()
            == "remote"
            for experience in location_results
        )

        print("✓ get_by_location_type() works")

        # ---------------------------------------------------------
        # 11. Delete
        # ---------------------------------------------------------
        exps = repository.get_all()
        expid = [
                    experience.id
                    for experience in exps
                ]
        for id in expid:
            datas = repository.get_by_id(id)
            repository.delete(datas)

        print("✓ delete() works")

        # ---------------------------------------------------------
        # 12. Verify Deleted Record
        # ---------------------------------------------------------
        for id in expid:            
            deleted = repository.get_by_id(id)
            assert deleted is None

        print("✓ Deleted experience is no longer retrievable")

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        print()
        print("=" * 60)
        print("Repository Verification Summary")
        print("=" * 60)

        print("✓ Repository initialization")
        print("✓ Model binding")
        print("✓ CRUD operations")
        print("✓ Ordered get_all()")
        print("✓ CRUD persistence")
        print("✓ get_current()")
        print("✓ get_by_company()")
        print("✓ get_by_company() is case-insensitive")
        print("✓ get_by_employment_type()")
        print("✓ get_by_location_type()")
        print("✓ Delete behaviour")

        print()
        print("🎉 ExperienceRepository verified successfully.")

    except AssertionError as exc:

        print()
        print("❌ Repository verification failed")

        if exc:
            print(exc)

        sys.exit(1)

    except Exception as exc:

        print()
        print("❌ Unexpected error")
        print(exc)

        sys.exit(1)

    finally:

        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------

        db.close()

    print("=" * 60)
    print("Repository verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()