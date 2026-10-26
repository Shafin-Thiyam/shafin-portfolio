import { useEffect, useState } from 'react'
import type { Experience } from '../../types/experience'
import { getExperiences } from '../../services/experiences'
import ExperienceCard from './ExperienceCard'

function ExperienceSection() {
  const [experiences, setExperiences] = useState<Experience[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadExperiences() {
      try {
        setIsLoading(true)
        setError(null)

        const experienceData = await getExperiences(controller.signal)

        setExperiences(experienceData)
      } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
          return
        }

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load professional experience.',
        )
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    void loadExperiences()

    return () => {
      controller.abort()
    }
  }, [])

  const sortedExperiences = [...experiences].sort(
    (a, b) => a.display_order - b.display_order,
  )

  return (
    <>
      {isLoading && (
        <p role="status" aria-live="polite">
          Loading professional experience...
        </p>
      )}

      {!isLoading && error && (
        <div role="alert">
          <p>We couldn't load your professional experience.</p>
          <p>{error}</p>
        </div>
      )}

      {!isLoading && !error && experiences.length === 0 && (
        <p>No professional experience is available at the moment.</p>
      )}

      {!isLoading && !error && sortedExperiences.length > 0 && (
        <div className="experience-grid">
          {sortedExperiences.map((experience) => (
            <ExperienceCard
              key={experience.id}
              experience={experience}
            />
          ))}
        </div>
      )}
    </>
  )
}

export default ExperienceSection