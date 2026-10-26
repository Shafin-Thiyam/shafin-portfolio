import type { Experience } from '../../types/experience'

interface ExperienceCardProps {
  experience: Experience
}

function formatEmploymentDate(date: string): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(`${date}T00:00:00Z`))
}

function ExperienceCard({ experience }: ExperienceCardProps) {
  const startDate = formatEmploymentDate(experience.start_date)

  const endDate = experience.is_current
    ? 'Present'
    : experience.end_date
      ? formatEmploymentDate(experience.end_date)
      : 'Not specified'

  return (
    <article className="experience-card">
      <div className="experience-card-header">
        <div>
          <h3 className="experience-designation">
            {experience.designation}
          </h3>

          <p className="experience-company">
            {experience.company}
          </p>
        </div>

        <span className="experience-employment-type">
          {experience.employment_type}
        </span>
      </div>

      <p className="experience-period">
        {startDate} – {endDate}
      </p>

      <p className="experience-location">
        {experience.location}
        {experience.location_type
          ? ` · ${experience.location_type}`
          : ''}
      </p>

      <p className="experience-description">
        {experience.description}
      </p>
    </article>
  )
}

export default ExperienceCard