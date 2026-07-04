"""
Verify ProfileRepository functionality.
"""
import sys
from app.db.session import SessionLocal
from app.models import Profile
from app.repositories import ProfileRepository


def main() -> None:
    """
    Verify ProfileRepository.
    """

    print("=" * 60)
    print("Profile Repository Verification")
    print("=" * 60)

    db = SessionLocal()

    try:
        repository = ProfileRepository(db)

        print("✓ Repository created successfully")

        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------

        existing = repository.get_profile()

        if existing:
            repository.delete(existing)

        print("✓ Existing profile cleaned")

        # ---------------------------------------------------------
        # Create Profile
        # ---------------------------------------------------------

        profile = Profile(
            full_name="Shafin Thiyam",
            title="Associate Consultant",
            email="shafin@example.com",
            phone="+91-9876543210",
            location="Hyderabad, India",
            linkedin_url="https://linkedin.com/in/shafin",
            github_url="https://github.com/Shafin-Thiyam",
            portfolio_url="https://shafin.dev",
            summary="Python Backend Developer",
            profile_image=None,
            resume_url=None,
        )

        repository.create(profile)

        print("✓ Profile created")
        print(f"  ID: {profile.id}")

        # ---------------------------------------------------------
        # Verify get_profile()
        # ---------------------------------------------------------

        stored_profile = repository.get_profile()

        assert stored_profile is not None
        assert stored_profile.email == "shafin@example.com"

        print("✓ get_profile()")
        
        # ---------------------------------------------------------
        # Verify get_by_id()
        # ---------------------------------------------------------

        profile_by_id = repository.get_by_id(profile.id)

        assert profile_by_id is not None
        assert profile_by_id.id == profile.id

        print("✓ get_by_id()")


        # ---------------------------------------------------------
        # Verify get_by_email()
        # ---------------------------------------------------------

        profile_by_email = repository.get_by_email(
            "shafin@example.com"
        )

        assert profile_by_email is not None
        assert profile_by_email.email == "shafin@example.com"

        print("✓ get_by_email()")
        
        # ---------------------------------------------------------
        # Verify get_all()
        # ---------------------------------------------------------

        profiles = repository.get_all()

        assert len(profiles) == 1

        print("✓ get_all()")
        
        # ---------------------------------------------------------
        # Verify count()
        # ---------------------------------------------------------

        count = repository.count()

        assert count == 1

        print("✓ count()")
        
        # ---------------------------------------------------------
        # Verify exists()
        # ---------------------------------------------------------

        exists = repository.exists(profile.id)

        assert exists is True

        print("✓ exists()")
        
        # ---------------------------------------------------------
        # Verify update()
        # ---------------------------------------------------------

        profile.title = "Senior Python Backend Developer"
        profile.location = "Bengaluru, India"

        updated_profile = repository.update(profile)

        assert updated_profile.title == "Senior Python Backend Developer"
        assert updated_profile.location == "Bengaluru, India"

        print("✓ update()")
        
        # ---------------------------------------------------------
        # Verify updated values
        # ---------------------------------------------------------

        stored_profile = repository.get_profile()

        assert stored_profile is not None
        assert stored_profile.title == "Senior Python Backend Developer"
        assert stored_profile.location == "Bengaluru, India"

        print("✓ Updated values verified")
        
        # ---------------------------------------------------------
        # Verify delete()
        # ---------------------------------------------------------

        repository.delete(profile)

        print("✓ delete()")

        # ---------------------------------------------------------
        # Verify profile removed
        # ---------------------------------------------------------

        deleted_profile = repository.get_profile()

        assert deleted_profile is None

        print("✓ Profile removed")
        
        # ---------------------------------------------------------
        # Verify exists()
        # ---------------------------------------------------------

        exists = repository.exists(profile.id)

        assert exists is False

        print("✓ exists() after delete")
        
        # ---------------------------------------------------------
        # Verify count()
        # ---------------------------------------------------------

        count = repository.count()

        assert count == 0

        print("✓ count() after delete")
        
        # ---------------------------------------------------------
        # Verify get_all()
        # ---------------------------------------------------------

        profiles = repository.get_all()

        assert len(profiles) == 0

        print("✓ get_all() after delete")
        
    except AssertionError as exc:
        print()
        print("❌ Verification failed")
        print(exc)
        sys.exit(1)

    except Exception as exc:
        print()
        print("❌ Unexpected error")
        print(exc)
        sys.exit(1)

    finally:
        db.close()

    print()
    print("=" * 60)
    print("Profile Repository Verification Summary")
    print("=" * 60)

    print("✓ create()")
    print("✓ get_profile()")
    print("✓ get_by_id()")
    print("✓ get_by_email()")
    print("✓ get_all()")
    print("✓ count()")
    print("✓ exists()")
    print("✓ update()")
    print("✓ delete()")

    print()
    print("🎉 All repository verification tests passed successfully.")
    print("=" * 60)

if __name__ == "__main__":
    main()