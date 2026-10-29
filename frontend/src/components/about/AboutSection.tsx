import type { Profile } from '../../types/profile'

interface AboutSectionProps {
  profile: Profile | null
  isLoading: boolean
  error: string | null
}

function AboutSection({
  profile,
  isLoading,
  error,
}: AboutSectionProps) {
  return (
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
  )
}

export default AboutSection
