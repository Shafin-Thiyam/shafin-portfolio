import type { Skill } from '../../types/skill'

interface SkillCategoryProps {
  category: string
  skills: Skill[]
}

function SkillCategory({ category, skills }: SkillCategoryProps) {
  return (
    <article className="skill-category-card">
      <h3 className="skill-category-title">{category}</h3>

      <div className="skill-list">
        {skills.map((skill) => (
          <div className="skill-item" key={skill.id}>
            <div className="skill-item-header">
              <span className="skill-name">{skill.name}</span>

              <span className="skill-proficiency">
                {skill.proficiency}%
              </span>
            </div>

            <div
              className="skill-progress-track"
              role="progressbar"
              aria-label={`${skill.name} proficiency`}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-valuenow={skill.proficiency}
            >
              <div
                className="skill-progress-fill"
                style={{ width: `${skill.proficiency}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </article>
  )
}

export default SkillCategory