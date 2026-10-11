
from pydantic import ValidationError

from app.schemas import ExperienceSkillsUpdate


def main() -> None:
    valid = ExperienceSkillsUpdate(
        skill_ids=[1, 3, 7],
    )
    assert valid.skill_ids == [1, 3, 7]

    empty = ExperienceSkillsUpdate(
        skill_ids=[],
    )
    assert empty.skill_ids == []

    for invalid_payload in (
        {"skill_ids": [1, 0, 3]},
        {"skill_ids": [1, -2]},
        {"skill_ids": "1,3,7"},
        {},
        {"skill_ids": [1], "unexpected": True},
    ):
        try:
            ExperienceSkillsUpdate.model_validate(
                invalid_payload
            )
        except ValidationError:
            continue

        raise AssertionError(
            f"Expected validation failure: {invalid_payload}"
        )

    print("Experience skills schema verification passed.")


if __name__ == "__main__":
    main()
