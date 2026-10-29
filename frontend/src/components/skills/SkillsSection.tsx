import { useEffect, useState } from 'react'
import type { Skill } from '../../types/skill'
import { getSkills } from '../../services/skills'
import SkillCategory from './SkillCategory'

function SkillsSection() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadSkills() {
      try {
        setIsLoading(true)
        setError(null)

        const skillData = await getSkills(controller.signal)

        setSkills(skillData)
      } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
          return
        }

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load skills.',
        )
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    void loadSkills()

    return () => {
      controller.abort()
    }
  }, [])

  const groupedSkills = skills.reduce<Record<string, Skill[]>>(
    (groups, skill) => {
      if (!groups[skill.category]) {
        groups[skill.category] = []
      }

      groups[skill.category].push(skill)

      return groups
    },
    {},
  )

  const sortedCategories = Object.entries(groupedSkills).sort(
    ([, skillsA], [, skillsB]) => {
      const orderA = Math.min(...skillsA.map((skill) => skill.display_order))
      const orderB = Math.min(...skillsB.map((skill) => skill.display_order))

      return orderA - orderB
    },
  )

  return (
    <section className="section skills-section" id="skills">
      <div className="container">
        <p className="eyebrow">TECHNICAL EXPERTISE</p>

        <h2>
          Skills & Technologies
        </h2>

        <p className="skills-description">
          Technologies and capabilities I've developed across software
          engineering, cloud platforms, data integration, and Generative AI.
        </p>

        {isLoading && (
          <p role="status" aria-live="polite">
            Loading skills...
          </p>
        )}

        {!isLoading && error && (
          <div role="alert">
            <p>We couldn't load your skills.</p>
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !error && skills.length === 0 && (
          <p>No skills are available at the moment.</p>
        )}

        {!isLoading && !error && skills.length > 0 && (
          <div className="skills-grid">
            {sortedCategories.map(([category, categorySkills]) => (
              <SkillCategory
                key={category}
                category={category}
                skills={categorySkills}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

export default SkillsSection