import { useEffect, useState } from 'react'
import Navigation from './components/navigation/Navigation'
import HeroSection from './components/hero/HeroSection'
import AboutSection from './components/about/AboutSection'
import ProjectsSection from './components/projects/ProjectsSection'
import ExperienceSection from './components/experience/ExperienceSection'
import SkillsSection from './components/skills/SkillsSection'
import { getProfile } from './services/profile'
import type { Profile } from './types/profile'
import './App.css'


function App() {
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
      <header className="site-header">
        <div className="container header-content">
          <a className="brand" href="#home" aria-label="Shafin Thiyam home">
            <img
              src="/images/shafinThiyam_logo.png"
              alt="Shafin Thiyam"
            />
          </a>

          <Navigation />

          <a className="header-cta" href="#contact">
            Let's Connect <span aria-hidden="true">↗</span>
          </a>
        </div>
      </header>

      <main>
        <HeroSection
          profile={profile}
          isLoading={isLoading}
          error={error}
        />

        <section className="expertise-section" aria-label="Core expertise">
          <div className="container expertise-grid">
            <article className="expertise-card">
              <span className="expertise-number">01</span>
              <h2>Backend Engineering</h2>
              <p>Python, FastAPI, Flask, Django and API design.</p>
            </article>

            <article className="expertise-card">
              <span className="expertise-number">02</span>
              <h2>Cloud & Platforms</h2>
              <p>AWS, SAP BTP, Kubernetes and Docker.</p>
            </article>

            <article className="expertise-card">
              <span className="expertise-number">03</span>
              <h2>Data & Integration</h2>
              <p>PostgreSQL, Snowflake, Kafka and enterprise integration.</p>
            </article>

            <article className="expertise-card">
              <span className="expertise-number">04</span>
              <h2>AI & LLM Engineering</h2>
              <p>LLMs, RAG, LangChain, MCP and AI agents.</p>
            </article>
          </div>
        </section>

        <AboutSection
          profile={profile}
          isLoading={isLoading}
          error={error}
          />

        <SkillsSection />

        <section className="section experience-section" id="experience">
          <div className="container">
            <p className="eyebrow">PROFESSIONAL JOURNEY</p>
            <h2>Experience & Growth</h2>
            <p>
              My professional journey across software engineering, cloud solutions,
              enterprise integration and AI initiatives.
            </p>

            <ExperienceSection />
          </div>
        </section>




        <section className="section projects-section" id="projects">
          <div className="container">
            <p className="eyebrow">SELECTED WORK</p>
            <h2>Projects that solve problems.</h2>
            <p>
              From cloud platforms to AI-powered applications, explore the
              work behind the ideas.
            </p>
            <ProjectsSection />

          </div>
        </section>

        <section className="section contact-section" id="contact">
          <div className="container contact-content">
            <div>
              <p className="eyebrow">LET'S CONNECT</p>
              <h2>
                Have an interesting
                <br />
                <span className="text-accent">problem to solve?</span>
              </h2>
              <p>
                Open to meaningful conversations, collaboration and
                opportunities to build something useful.
              </p>
            </div>

            <a className="button button-primary" href="mailto:">
              Get in Touch <span aria-hidden="true">→</span>
            </a>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="container footer-content">
          <p>© {new Date().getFullYear()} Shafin Thiyam</p>
          <p>Designed with purpose. Built with curiosity.</p>
        </div>
      </footer>
    </>
  )
}

export default App