export interface Experience {
  id: number
  company: string
  designation: string
  employment_type: string
  location: string
  location_type: string
  start_date: string
  end_date: string | null
  is_current: boolean
  description: string
  display_order: number
  created_at: string
  updated_at: string
}