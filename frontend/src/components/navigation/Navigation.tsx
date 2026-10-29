import { useEffect, useState } from 'react'

const navigationItems = [
  { label: 'Home', href: '#home' },
  { label: 'About', href: '#about' },
  { label: 'Skills', href: '#skills' },
  { label: 'Experience', href: '#experience' },
  { label: 'Projects', href: '#projects' },
  { label: 'Contact', href: '#contact' },
]

function Navigation() {
  const [activeSection, setActiveSection] = useState('home')

  useEffect(() => {
    const sectionElements = navigationItems
      .map((item) => document.getElementById(item.href.slice(1)))
      .filter((section): section is HTMLElement => section !== null)

    if (sectionElements.length === 0) {
      return
    }

    let animationFrame = 0

    const updateActiveSection = () => {
      cancelAnimationFrame(animationFrame)

      animationFrame = requestAnimationFrame(() => {
        const activationPoint = window.innerHeight * 0.3

        let currentSection = sectionElements[0]

        for (const section of sectionElements) {
          const sectionTop = section.getBoundingClientRect().top

          if (sectionTop <= activationPoint) {
            currentSection = section
          } else {
            break
          }
        }

        setActiveSection(currentSection.id)
      })
    }

    window.addEventListener('scroll', updateActiveSection, {
      passive: true,
    })
    window.addEventListener('resize', updateActiveSection)

    // Set the correct active link when the page first loads.
    updateActiveSection()

    // Recheck after a navigation link changes the URL fragment.
    window.addEventListener('hashchange', updateActiveSection)

    return () => {
      cancelAnimationFrame(animationFrame)
      window.removeEventListener('scroll', updateActiveSection)
      window.removeEventListener('resize', updateActiveSection)
      window.removeEventListener('hashchange', updateActiveSection)
    }
  }, [])

  return (
    <nav className="main-nav" aria-label="Main navigation">
      {navigationItems.map((item) => {
        const sectionId = item.href.slice(1)
        const isActive = activeSection === sectionId

        return (
          <a
            key={item.href}
            className={`nav-link${isActive ? ' active' : ''}`}
            href={item.href}
            aria-current={isActive ? 'location' : undefined}
          >
            {item.label}
          </a>
        )
      })}
    </nav>
  )
}

export default Navigation