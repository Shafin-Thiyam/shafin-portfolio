import type { ApiResponse } from '../types/project'
import type { Experience } from '../types/experience'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
).replace(/\/+$/, '')

export async function getExperiences(
  signal?: AbortSignal,
): Promise<Experience[]> {
  const response = await fetch(`${API_BASE_URL}/experiences`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
    signal,
  })

  if (!response.ok) {
    throw new Error(
      `Unable to load experiences (HTTP ${response.status}).`,
    )
  }

  const result: ApiResponse<Experience[]> = await response.json()

  if (!result.success || !Array.isArray(result.data)) {
    throw new Error('The experiences API returned an unexpected response.')
  }

  return result.data
}