import type { Profile } from '../../types/profile'

interface HeroSectionProps {
  profile: Profile | null
  isLoading: boolean
  error: string | null
}

function HeroSection({
  profile,
  isLoading,
  error,
}: HeroSectionProps) {
  return (
    <section className="hero-section" id="home">
      <div className="container hero-content">
        <div className="hero-copy">
          <p className="eyebrow">
            SOFTWARE ENGINEER <span>•</span> CLOUD ARCHITECT{' '}
            <span>•</span> AI EXPLORER
          </p>

          <h1>
            Engineering
            <br />
            intelligent solutions.
            <br />
            <span className="text-accent">
              Building what comes next.
            </span>
          </h1>

          {isLoading && (
            <p className="hero-description" role="status">
              Loading profile...
            </p>
          )}

          {!isLoading && error && (
            <p className="hero-description" role="alert">
              Profile information is temporarily unavailable.
            </p>
          )}

          {!isLoading && !error && profile && (
            <p className="hero-profile-title">
              {profile.full_name} · {profile.title}
            </p>
          )}

          {!isLoading && !error && profile && (
            <p className="hero-description">
              {profile.summary}
            </p>
          )}

          <div className="hero-actions">
            <a className="button button-primary" href="#projects">
              Explore My Work <span aria-hidden="true">→</span>
            </a>

            <a className="button button-outline" href="#experience">
              View Experience
            </a>
          </div>

          <div className="hero-note">
            <span className="status-dot" aria-hidden="true" />
            Building practical solutions with curiosity and purpose.
          </div>
        </div>

        <div className="hero-visual" aria-hidden="true">
          <div className="visual-orbit orbit-one" />
          <div className="visual-orbit orbit-two" />

          <div className="visual-card">
            <span className="visual-card-label">MY APPROACH</span>
            <span className="visual-card-title">
              Better Problems.
              <br />
              Bigger Learnings.
            </span>
            <span className="visual-card-line" />
            <span className="visual-card-footer">
              ENGINEER · EXPLORE · BUILD
            </span>
          </div>

          <span className="floating-tag tag-python">Python</span>
          <span className="floating-tag tag-cloud">Cloud</span>
          <span className="floating-tag tag-ai">Generative AI</span>
        </div>
      </div>
    </section>
  )
}

export default HeroSection