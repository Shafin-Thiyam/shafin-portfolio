import ProjectsSection from './components/projects/ProjectsSection'
import './App.css'


function App() {
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

          <nav className="main-nav" aria-label="Main navigation">
            <a className="nav-link active" href="#home">Home</a>
            <a className="nav-link" href="#about">About</a>
            <a className="nav-link" href="#experience">Experience</a>
            <a className="nav-link" href="#projects">Projects</a>
            <a className="nav-link" href="#contact">Contact</a>
          </nav>

          <a className="header-cta" href="#contact">
            Let's Connect <span aria-hidden="true">↗</span>
          </a>
        </div>
      </header>

      <main>
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

              <p className="hero-description">
                I'm Shafin Thiyam, a software engineer and cloud solutions
                architect with 13+ years of experience. I work across Python,
                cloud platforms, enterprise integration, and Generative AI —
                turning complex challenges into practical, scalable solutions.
              </p>

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

        <section className="section intro-section" id="about">
          <div className="container">
            <p className="eyebrow">A LITTLE ABOUT ME</p>
            <h2>
              Engineering with purpose.
              <br />
              <span className="text-accent">
                Learning without limits.
              </span>
            </h2>
            <p className="intro-description">
              I enjoy solving real-world engineering problems, exploring
              emerging technologies, and building maintainable applications
              that turn ideas into useful solutions.
            </p>
          </div>
        </section>

        <section className="section experience-section" id="experience">
          <div className="container">
            <p className="eyebrow">PROFESSIONAL JOURNEY</p>
            <h2>Experience & Growth</h2>
            <p>
              13+ years across software engineering, cloud solutions,
              enterprise integration and AI initiatives.
            </p>
            <p className="section-hint">
              We'll connect this section to your portfolio API in a later step.
            </p>
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