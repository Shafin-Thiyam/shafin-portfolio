import type { ApiResponse, Project } from '../types/project'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
).replace(/\/+$/, '')

export async function getProjects(
  signal?: AbortSignal,
): Promise<Project[]> {
  const response = await fetch(`${API_BASE_URL}/projects`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
    signal,
  })

  if (!response.ok) {
    throw new Error(`Unable to load projects (HTTP ${response.status}).`)
  }

  const result: ApiResponse<Project[]> = await response.json()

  if (!result.success || !Array.isArray(result.data)) {
    throw new Error('The projects API returned an unexpected response.')
  }

  return result.data
}
