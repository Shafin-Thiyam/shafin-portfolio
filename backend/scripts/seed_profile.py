"""
Seed the Profile table.

Run:

    python -m scripts.seed_profile
"""

from app.db import SessionLocal
from app.models import Profile
from app.repositories import ProfileRepository


def seed_profile() -> None:
    """
    Seed the Profile table.
    """

    db = SessionLocal()

    try:
        repository = ProfileRepository(db)
        
        existing_profile = repository.get_profile()
        
        if existing_profile is not None:
            print("✓ Seed skipped (profile already exists).")
            return

        profile = Profile(
            full_name="Shafin Thiyam",
            title="Associate Consultant",
            email="shafin.thiyam@outlook.com",
            phone="+91-879068939",
            location="Hyderabad, India",
            linkedin_url="https://in.linkedin.com/in/shafinthiyam",
            github_url="https://github.com/Shafin-Thiyam",
            portfolio_url="https://portfolio.example.com",
            summary=(
                "Experienced Python Backend Developer with expertise "
                "in FastAPI, SAP BTP, Docker, Kubernetes, and PostgreSQL."
            ),
            profile_image=None,
            resume_url=None,
        )

        repository.create(profile)

        print("✓ Profile seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_profile()