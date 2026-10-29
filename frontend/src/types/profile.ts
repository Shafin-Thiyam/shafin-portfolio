export interface Profile {
  id: number
  full_name: string
  title: string
  email: string
  phone: string
  location: string
  linkedin_url: string
  github_url: string
  portfolio_url: string
  summary: string
  profile_image: string
  resume_url: string
  created_at: string
  updated_at: string
}

export interface ApiResponse<T> {
  success: boolean
  message: string
  data: T | null
}