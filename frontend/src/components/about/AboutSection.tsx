import { useEffect, useState } from 'react'
import type { Profile } from '../../types/profile'
import { getProfile } from '../../services/profile'

function AboutSection() {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadProfile() {
      try {
        setIsLoading(true)
        setError(null)

        const profileData = await getProfile(controller.signal)
        setProfile(profileData)
      } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
          return
        }

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load profile information.',
        )
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    void loadProfile()

    return () => {
      controller.abort()
    }
  }, [])

  return (
    <>
    <section className="section intro-section" id="about">
      <div className="container">
        <p className="eyebrow">A LITTLE ABOUT ME</p>

        <h2>
          Engineering with purpose.
          <br />
          <span className="text-accent">Learning without limits.</span>
        </h2>

        {isLoading && (
          <p role="status" aria-live="polite">
            Loading profile...
          </p>
        )}

        {!isLoading && error && (
          <div role="alert">
            <p>We couldn't load your profile.</p>
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !error && profile && (
          <div className="about-content">
            <p className="about-title">{profile.title}</p>

            <p className="intro-description">
              {profile.summary}
            </p>

            <p className="about-location">{profile.location}</p>
          </div>
        )}
      </div>
    </section>
    </>
  )
}

export default AboutSection