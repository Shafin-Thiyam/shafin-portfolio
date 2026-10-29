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
  const [isMenuOpen, setIsMenuOpen] = useState(false)

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
          if (section.getBoundingClientRect().top <= activationPoint) {
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
    window.addEventListener('hashchange', updateActiveSection)

    updateActiveSection()

    return () => {
      cancelAnimationFrame(animationFrame)
      window.removeEventListener('scroll', updateActiveSection)
      window.removeEventListener('resize', updateActiveSection)
      window.removeEventListener('hashchange', updateActiveSection)
    }
  }, [])

  useEffect(() => {
    // Close the mobile menu when returning to desktop width.
    const handleResize = () => {
      if (window.innerWidth > 760) {
        setIsMenuOpen(false)
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  useEffect(() => {
    if (!isMenuOpen) {
      return
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsMenuOpen(false)
      }
    }

    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isMenuOpen])

  const closeMenu = () => setIsMenuOpen(false)

  return (
    <>
      <button
        type="button"
        className="menu-toggle"
        aria-label={isMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
        aria-expanded={isMenuOpen}
        aria-controls="primary-navigation"
        onClick={() => setIsMenuOpen((open) => !open)}
      >
        <span />
        <span />
        <span />
      </button>

      <nav
        id="primary-navigation"
        className={`main-nav${isMenuOpen ? ' is-open' : ''}`}
        aria-label="Main navigation"
      >
        {navigationItems.map((item) => {
          const sectionId = item.href.slice(1)
          const isActive = activeSection === sectionId

          return (
            <a
              key={item.href}
              className={`nav-link${isActive ? ' active' : ''}`}
              href={item.href}
              aria-current={isActive ? 'location' : undefined}
              onClick={closeMenu}
            >
              {item.label}
            </a>
          )
        })}
      </nav>
    </>
  )
}

export default Navigation
