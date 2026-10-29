import type { Skill } from '../types/skill'

interface ApiResponse<T> {
  success: boolean
  message: string
  data: T | null
}

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
).replace(/\/+$/, '')

export async function getSkills(
  signal?: AbortSignal,
): Promise<Skill[]> {
  const response = await fetch(`${API_BASE_URL}/skills`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
    signal,
  })

  if (!response.ok) {
    throw new Error(`Unable to load skills (HTTP ${response.status}).`)
  }

  const result: ApiResponse<Skill[]> = await response.json()

  if (!result.success || !Array.isArray(result.data)) {
    throw new Error('The skills API returned an unexpected response.')
  }

  return result.data
}