export interface Project {
  id: number
  experience_id: number
  title: string
  description: string | null
  role: string | null
  technologies: string[]
  project_url: string | null
  repository_url: string | null
  start_date: string | null
  end_date: string | null
  display_order: number
  created_at: string
  updated_at: string
}

export interface ApiResponse<T> {
  success: boolean
  message: string
  data: T | null
}
