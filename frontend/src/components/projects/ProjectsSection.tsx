import { useEffect, useState } from 'react'
import type { Project } from '../../types/project'
import type { Experience } from '../../types/experience'
import { getProjects } from '../../services/projects'
import { getExperiences } from '../../services/experiences'
import ProjectCard from './ProjectCard'

function ProjectsSection() {
  const [projects, setProjects] = useState<Project[]>([])
  const [experiences, setExperiences] = useState<Experience[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadPortfolioData() {
      try {
        setIsLoading(true)
        setError(null)

        const [projectData, experienceData] = await Promise.all([
          getProjects(controller.signal),
          getExperiences(controller.signal),
        ])

        setProjects(projectData)
        setExperiences(experienceData)
      } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
          return
        }

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load portfolio projects.',
        )
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    void loadPortfolioData()

    return () => {
      controller.abort()
    }
  }, [])

  const experienceById = new Map(
    experiences.map((experience) => [experience.id, experience]),
  )

  return (
    <>

        {isLoading && (
          <p role="status" aria-live="polite">
            Loading projects...
          </p>
        )}

        {!isLoading && error && (
          <div role="alert">
            <p>We couldn't load the projects.</p>
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !error && projects.length === 0 && (
          <p>No projects are available at the moment.</p>
        )}

        {!isLoading && !error && projects.length > 0 && (
          <div className="projects-grid">
            {projects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                experience={experienceById.get(project.experience_id)}
              />
            ))}
          </div>
        )}
      </>

  )
}

export default ProjectsSection