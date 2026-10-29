import type { ApiResponse, Profile } from '../types/profile'


const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
).replace(/\/+$/, '')

export async function getProfile(
  signal?: AbortSignal,
): Promise<Profile> {
  const response = await fetch(`${API_BASE_URL}/profile`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
    signal,
  })

  if (!response.ok) {
    throw new Error(`Unable to load profile (HTTP ${response.status}).`)
  }

  const result: ApiResponse<Profile> = await response.json()

  if (!result.success || !result.data) {
    throw new Error('The profile API returned an unexpected response.')
  }

  return result.data
}