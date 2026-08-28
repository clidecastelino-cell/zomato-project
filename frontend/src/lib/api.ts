const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface FilterOptions {
  locations: string[];
  cuisines: string[];
  max_rating: number;
}

export interface RecommendationRequest {
  location: string;
  budget: string;
  min_rating: number;
  cuisines: string[];
  additional_preferences: string;
}

export interface RecommendationResult {
  name: string;
  rating: number;
  cost: string;
  cuisines: string;
  explanation: string;
}

export async function fetchFilters(): Promise<FilterOptions> {
  const res = await fetch(`${API_BASE_URL}/api/filters`);
  if (!res.ok) {
    throw new Error('Failed to fetch filters');
  }
  return res.json();
}

export async function fetchRecommendations(req: RecommendationRequest): Promise<RecommendationResult[]> {
  const res = await fetch(`${API_BASE_URL}/api/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  });
  
  if (!res.ok) {
    let errorMessage = 'Failed to fetch recommendations';
    try {
      const errorData = await res.json();
      if (errorData.detail) errorMessage = errorData.detail;
    } catch (e) {
      // ignore JSON parse error
    }
    throw new Error(errorMessage);
  }
  
  const data = await res.json();
  return data.recommendations;
}
