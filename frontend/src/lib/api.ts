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
  preferred_cuisines: string[];
  additional_preferences: string;
}

export interface RecommendationResult {
  restaurant: any; // We can type this strictly based on Zomato dataset if needed
  match_score: number;
  match_reason: string;
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
    throw new Error('Failed to fetch recommendations');
  }
  
  const data = await res.json();
  return data.recommendations;
}
