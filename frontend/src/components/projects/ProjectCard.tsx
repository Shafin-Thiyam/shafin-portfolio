import type { Project } from '../../types/project'
import type { Experience } from '../../types/experience'

interface ProjectCardProps {
  project: Project
  experience?: Experience
}

function ProjectCard({ project, experience }: ProjectCardProps) {
  return (
    <article className="project-card">
      <div className="project-card-header">
        <span className="project-label">PROJECT</span>

        <h3 className="project-title">{project.title}</h3>
      </div>

      <div className="project-company">
        <span className="project-meta-label">Company / Client</span>
        <p>{experience?.company ?? 'Company not specified'}</p>
      </div>

      <div className="project-role">
        <span className="project-meta-label">Role</span>
        <p>{experience?.designation ?? project.role ?? 'Role not specified'}</p>
      </div>

      {project.description && (
        <p className="project-description">{project.description}</p>
      )}

      {project.technologies.length > 0 && (
        <div className="project-technologies" aria-label="Technologies used">
          {project.technologies.map((technology) => (
            <span className="technology-badge" key={technology}>
              {technology}
            </span>
          ))}
        </div>
      )}

      {(project.project_url || project.repository_url) && (
        <div className="project-links">
          {project.project_url && (
            <a
              href={project.project_url}
              target="_blank"
              rel="noreferrer"
            >
              View project ↗
            </a>
          )}

          {project.repository_url && (
            <a
              href={project.repository_url}
              target="_blank"
              rel="noreferrer"
            >
              Source code ↗
            </a>
          )}
        </div>
      )}
    </article>
  )
}

export default ProjectCard