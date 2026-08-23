"""
Verify ExperienceService behavior.

This script verifies:
    - Experience retrieval
    - Experience CRUD
    - Duplicate validation
    - Missing experience validation
    - Skill queries
    - Skill management
    - Skill replacement
    - Skill clearing
    - Missing skill validation
    - Relationship validation
"""

from datetime import date

from app.db import SessionLocal
from app.schemas import (
    ExperienceCreate,
    ExperienceUpdate,
)
from app.services import ExperienceService


# ============================================================
# Test constants
# ============================================================

TEST_COMPANY = "__SERVICE_TEST_COMPANY__"
TEST_COMPANY_2 = "__SERVICE_TEST_COMPANY_2__"

TEST_DESIGNATION = "__SERVICE_TEST_DESIGNATION__"
TEST_DESIGNATION_2 = "__SERVICE_TEST_DESIGNATION_2__"

TEST_START_DATE = date(2026, 1, 1)

TEST_DISPLAY_ORDER = 999999

INVALID_EXPERIENCE_ID = -999999
INVALID_SKILL_ID = -999999


# ============================================================
# Assertion helpers
# ============================================================

def assert_equal(
    actual,
    expected,
    message: str,
) -> None:
    """
    Assert that two values are equal.
    """

    if actual != expected:
        raise AssertionError(
            f"{message} | "
            f"expected={expected!r}, "
            f"actual={actual!r}"
        )


def assert_true(
    value: bool,
    message: str,
) -> None:
    """
    Assert that a condition is true.
    """

    if not value:
        raise AssertionError(message)


def assert_raises(
    exception_type,
    function,
    message: str,
) -> None:
    """
    Verify that a function raises the expected exception.
    """

    try:
        function()
    except exception_type:
        return

    raise AssertionError(
        f"{message} | "
        f"expected {exception_type.__name__}"
    )


# ============================================================
# Test data builders
# ============================================================

def build_experience(
    company: str = TEST_COMPANY,
    designation: str = TEST_DESIGNATION,
    start_date: date = TEST_START_DATE,
) -> ExperienceCreate:
    """
    Build test experience data.
    """

    return ExperienceCreate(
        company=company,
        designation=designation,
        employment_type="Full-time",
        location="Test Location",
        location_type="Remote",
        start_date=start_date,
        end_date=None,
        is_current=True,
        description="Service verification test record.",
        display_order=TEST_DISPLAY_ORDER,
    )


# ============================================================
# Main verification
# ============================================================

def main() -> None:
    """
    Execute ExperienceService verification.
    """

    db = SessionLocal()
    service = ExperienceService(db)

    created_experience_ids: list[int] = []

    try:
        print("Starting ExperienceService verification...")

        # =====================================================
        # 1. Basic retrieval
        # =====================================================

        print("\n[1] Basic retrieval")

        experiences = service.get_all()

        assert_true(
            isinstance(experiences, list),
            "get_all() should return a list.",
        )

        print("PASS: get_all()")

        current_experiences = service.get_current()

        assert_true(
            isinstance(current_experiences, list),
            "get_current() should return a list.",
        )

        print("PASS: get_current()")

        company_experiences = service.get_by_company(
            TEST_COMPANY
        )

        assert_true(
            isinstance(company_experiences, list),
            "get_by_company() should return a list.",
        )

        print("PASS: get_by_company()")

        employment_experiences = (
            service.get_by_employment_type(
                "Full-time"
            )
        )

        assert_true(
            isinstance(employment_experiences, list),
            "get_by_employment_type() should return a list.",
        )

        print("PASS: get_by_employment_type()")

        location_experiences = (
            service.get_by_location_type(
                "Remote"
            )
        )

        assert_true(
            isinstance(location_experiences, list),
            "get_by_location_type() should return a list.",
        )

        print("PASS: get_by_location_type()")

        # =====================================================
        # 2. Experience CRUD - Create
        # =====================================================

        print("\n[2] Experience CRUD")

        experience_data = build_experience()

        experience = service.create(
            experience_data
        )

        created_experience_ids.append(
            experience.id
        )

        assert_true(
            experience.id is not None,
            "Created experience should have an ID.",
        )

        assert_equal(
            experience.company,
            TEST_COMPANY,
            "Created company mismatch.",
        )

        assert_equal(
            experience.designation,
            TEST_DESIGNATION,
            "Created designation mismatch.",
        )

        print("PASS: create()")

        # =====================================================
        # 3. Get by ID
        # =====================================================

        retrieved = service.get_by_id(
            experience.id
        )

        assert_true(
            retrieved is not None,
            "Created experience should be retrievable.",
        )

        assert_equal(
            retrieved.id,
            experience.id,
            "Retrieved experience ID mismatch.",
        )

        print("PASS: get_by_id()")

        # =====================================================
        # 4. Duplicate validation
        # =====================================================

        print("\n[3] Duplicate validation")

        duplicate_data = build_experience()

        assert_raises(
            ValueError,
            lambda: service.create(
                duplicate_data
            ),
            "Duplicate experience creation should fail.",
        )

        print("PASS: duplicate create validation")

        # =====================================================
        # 5. Update
        # =====================================================

        update_data = ExperienceUpdate(
            company=TEST_COMPANY,
            designation=TEST_DESIGNATION_2,
            employment_type="Full-time",
            location="Updated Location",
            location_type="Hybrid",
            start_date=TEST_START_DATE,
            end_date=None,
            is_current=True,
            description="Updated service verification record.",
            display_order=TEST_DISPLAY_ORDER,
        )

        updated = service.update(
            experience.id,
            update_data,
        )

        assert_equal(
            updated.designation,
            TEST_DESIGNATION_2,
            "Updated designation mismatch.",
        )

        assert_equal(
            updated.location,
            "Updated Location",
            "Updated location mismatch.",
        )

        print("PASS: update()")

        # =====================================================
        # 6. Same-record update should be allowed
        # =====================================================

        same_record_update = ExperienceUpdate(
            company=TEST_COMPANY,
            designation=TEST_DESIGNATION_2,
            employment_type="Full-time",
            location="Updated Location",
            location_type="Hybrid",
            start_date=TEST_START_DATE,
            end_date=None,
            is_current=True,
            description="Updated again.",
            display_order=TEST_DISPLAY_ORDER,
        )

        service.update(
            experience.id,
            same_record_update,
        )

        print("PASS: same-record update")

        # =====================================================
        # 7. Duplicate update validation
        # =====================================================

        second_experience_data = build_experience(
            company=TEST_COMPANY_2,
            designation=TEST_DESIGNATION,
        )

        second_experience = service.create(
            second_experience_data
        )

        created_experience_ids.append(
            second_experience.id
        )

        duplicate_update_data = ExperienceUpdate(
            company=TEST_COMPANY,
            designation=TEST_DESIGNATION_2,
            employment_type="Full-time",
            location="Another Location",
            location_type="Remote",
            start_date=TEST_START_DATE,
            end_date=None,
            is_current=True,
            description="Duplicate update test.",
            display_order=TEST_DISPLAY_ORDER,
        )

        assert_raises(
            ValueError,
            lambda: service.update(
                second_experience.id,
                duplicate_update_data,
            ),
            "Duplicate experience update should fail.",
        )

        print("PASS: duplicate update validation")

        # =====================================================
        # 8. Missing experience validation
        # =====================================================

        print("\n[4] Missing experience validation")

        assert_raises(
            ValueError,
            lambda: service.update(
                INVALID_EXPERIENCE_ID,
                update_data,
            ),
            "Updating missing experience should fail.",
        )

        print("PASS: missing experience update")

        assert_raises(
            ValueError,
            lambda: service.get_skill_ids(
                INVALID_EXPERIENCE_ID
            ),
            "Getting skills for missing experience should fail.",
        )

        print("PASS: missing experience get_skill_ids()")

        assert_raises(
            ValueError,
            lambda: service.delete(
                INVALID_EXPERIENCE_ID
            ),
            "Deleting missing experience should fail.",
        )

        print("PASS: missing experience delete")

        # =====================================================
        # 9. Skill queries
        # =====================================================

        print("\n[5] Skill queries")

        skill_ids = service.get_skill_ids(
            experience.id
        )

        assert_true(
            isinstance(skill_ids, list),
            "get_skill_ids() should return a list.",
        )

        print("PASS: get_skill_ids()")

        # =====================================================
        # 10. Skill management
        # =====================================================

        print("\n[6] Skill management")

        skills = service.skill_repository.get_all()

        if not skills:
            print(
                "SKIP: Skill management tests "
                "because no skills exist."
            )

        else:
            skill = skills[0]

            # -------------------------------------------------
            # Add skill
            # -------------------------------------------------

            service.add_skill(
                experience.id,
                skill.id,
            )

            skill_ids = service.get_skill_ids(
                experience.id
            )

            assert_true(
                skill.id in skill_ids,
                "Skill should be associated.",
            )

            print("PASS: add_skill()")

            # -------------------------------------------------
            # Duplicate association
            # -------------------------------------------------

            assert_raises(
                ValueError,
                lambda: service.add_skill(
                    experience.id,
                    skill.id,
                ),
                "Duplicate skill association should fail.",
            )

            print(
                "PASS: duplicate skill association"
            )

            # -------------------------------------------------
            # Skill ID query
            # -------------------------------------------------

            experiences_by_skill = (
                service.get_by_skill_id(
                    skill.id
                )
            )

            assert_true(
                any(
                    item.id == experience.id
                    for item in experiences_by_skill
                ),
                "Experience should be returned by skill ID.",
            )

            print("PASS: get_by_skill_id()")

            # -------------------------------------------------
            # Skill name query
            # -------------------------------------------------

            experiences_by_skill_name = (
                service.get_by_skill_name(
                    skill.name
                )
            )

            assert_true(
                any(
                    item.id == experience.id
                    for item in experiences_by_skill_name
                ),
                "Experience should be returned by skill name.",
            )

            print("PASS: get_by_skill_name()")

            # -------------------------------------------------
            # Remove skill
            # -------------------------------------------------

            service.remove_skill(
                experience.id,
                skill.id,
            )

            skill_ids = service.get_skill_ids(
                experience.id
            )

            assert_true(
                skill.id not in skill_ids,
                "Skill should be removed.",
            )

            print("PASS: remove_skill()")

            # -------------------------------------------------
            # Removing again should fail
            # -------------------------------------------------

            assert_raises(
                ValueError,
                lambda: service.remove_skill(
                    experience.id,
                    skill.id,
                ),
                "Removing unassociated skill should fail.",
            )

            print(
                "PASS: remove unassociated skill"
            )

            # -------------------------------------------------
            # Missing skill validation
            # -------------------------------------------------

            assert_raises(
                ValueError,
                lambda: service.add_skill(
                    experience.id,
                    INVALID_SKILL_ID,
                ),
                "Adding missing skill should fail.",
            )

            print("PASS: missing skill add validation")

            assert_raises(
                ValueError,
                lambda: service.remove_skill(
                    experience.id,
                    INVALID_SKILL_ID,
                ),
                "Removing missing skill should fail.",
            )

            print("PASS: missing skill remove validation")

            # -------------------------------------------------
            # Missing experience skill operations
            # -------------------------------------------------

            assert_raises(
                ValueError,
                lambda: service.add_skill(
                    INVALID_EXPERIENCE_ID,
                    skill.id,
                ),
                "Adding skill to missing experience should fail.",
            )

            print(
                "PASS: missing experience add_skill()"
            )

            assert_raises(
                ValueError,
                lambda: service.remove_skill(
                    INVALID_EXPERIENCE_ID,
                    skill.id,
                ),
                "Removing skill from missing experience should fail.",
            )

            print(
                "PASS: missing experience remove_skill()"
            )

            # =================================================
            # 11. set_skills()
            # =================================================

            print("\n[7] Skill replacement")

            if len(skills) >= 2:
                skill_1 = skills[0]
                skill_2 = skills[1]

                # ---------------------------------------------
                # Set multiple skills
                # ---------------------------------------------

                service.set_skills(
                    experience.id,
                    [
                        skill_1.id,
                        skill_2.id,
                    ],
                )

                skill_ids = service.get_skill_ids(
                    experience.id
                )

                assert_equal(
                    set(skill_ids),
                    {
                        skill_1.id,
                        skill_2.id,
                    },
                    "set_skills() should replace skill associations.",
                )

                print("PASS: set_skills()")

                # ---------------------------------------------
                # Duplicate IDs should be removed
                # ---------------------------------------------

                service.set_skills(
                    experience.id,
                    [
                        skill_1.id,
                        skill_1.id,
                        skill_2.id,
                        skill_2.id,
                    ],
                )

                skill_ids = service.get_skill_ids(
                    experience.id
                )

                assert_equal(
                    set(skill_ids),
                    {
                        skill_1.id,
                        skill_2.id,
                    },
                    "set_skills() should remove duplicate IDs.",
                )

                assert_equal(
                    len(skill_ids),
                    2,
                    "set_skills() should not create duplicate relationships.",
                )

                print(
                    "PASS: set_skills() duplicate IDs"
                )

                # ---------------------------------------------
                # Invalid skill should fail
                # ---------------------------------------------

                before_skill_ids = (
                    service.get_skill_ids(
                        experience.id
                    )
                )

                assert_raises(
                    ValueError,
                    lambda: service.set_skills(
                        experience.id,
                        [
                            skill_1.id,
                            INVALID_SKILL_ID,
                        ],
                    ),
                    "set_skills() with missing skill should fail.",
                )

                print(
                    "PASS: set_skills() missing skill validation"
                )

                # ---------------------------------------------
                # Failed set_skills() should not modify
                # existing relationships
                # ---------------------------------------------

                after_skill_ids = (
                    service.get_skill_ids(
                        experience.id
                    )
                )

                assert_equal(
                    set(after_skill_ids),
                    set(before_skill_ids),
                    "Failed set_skills() should not modify relationships.",
                )

                print(
                    "PASS: set_skills() failed operation preserves relationships"
                )

                # ---------------------------------------------
                # Missing experience
                # ---------------------------------------------

                assert_raises(
                    ValueError,
                    lambda: service.set_skills(
                        INVALID_EXPERIENCE_ID,
                        [
                            skill_1.id,
                            skill_2.id,
                        ],
                    ),
                    "set_skills() for missing experience should fail.",
                )

                print(
                    "PASS: set_skills() missing experience validation"
                )

                # =================================================
                # 12. clear_skills()
                # =================================================

                print("\n[8] Clear skills")

                service.clear_skills(
                    experience.id
                )

                skill_ids = service.get_skill_ids(
                    experience.id
                )

                assert_equal(
                    skill_ids,
                    [],
                    "clear_skills() should remove all skill associations.",
                )

                print("PASS: clear_skills()")

                # ---------------------------------------------
                # Missing experience
                # ---------------------------------------------

                assert_raises(
                    ValueError,
                    lambda: service.clear_skills(
                        INVALID_EXPERIENCE_ID
                    ),
                    "clear_skills() for missing experience should fail.",
                )

                print(
                    "PASS: clear_skills() missing experience validation"
                )

            else:
                print(
                    "SKIP: set_skills() and clear_skills() "
                    "tests because fewer than 2 skills exist."
                )

        # =====================================================
        # 13. Delete
        # =====================================================

        print("\n[9] Delete")

        service.delete(
            experience.id
        )

        deleted = service.get_by_id(
            experience.id
        )

        assert_equal(
            deleted,
            None,
            "Deleted experience should not exist.",
        )

        print("PASS: delete()")

        created_experience_ids.remove(
            experience.id
        )

        print(
            "\nExperienceService verification PASSED."
        )

    finally:
        # =====================================================
        # Cleanup
        # =====================================================

        for experience_id in created_experience_ids:
            try:
                service.delete(
                    experience_id
                )
            except ValueError:
                pass

        db.close()


if __name__ == "__main__":
    main()