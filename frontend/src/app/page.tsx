"use client";

import { useState, useEffect } from "react";
import { fetchFilters, fetchRecommendations, FilterOptions, RecommendationResult } from "@/lib/api";

export default function Home() {
  const [filters, setFilters] = useState<FilterOptions | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [location, setLocation] = useState("");
  const [budget, setBudget] = useState("Any");
  const [minRating, setMinRating] = useState(4.0);
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [preferences, setPreferences] = useState("");
  
  const [recommendations, setRecommendations] = useState<RecommendationResult[]>([]);
  const [isRecommending, setIsRecommending] = useState(false);

  useEffect(() => {
    fetchFilters()
      .then((data) => {
        setFilters(data);
        if (data.locations.length > 0) setLocation(data.locations[0]);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const toggleCuisine = (c: string) => {
    setSelectedCuisines((prev) =>
      prev.includes(c) ? prev.filter((item) => item !== c) : [...prev, c]
    );
  };

  const getRecommendations = async () => {
    setIsRecommending(true);
    try {
      const results = await fetchRecommendations({
        location,
        budget,
        min_rating: minRating,
        cuisines: selectedCuisines,
        additional_preferences: preferences,
      });
      setRecommendations(results);
    } catch (err: any) {
      alert("Failed to get recommendations: " + err.message);
    } finally {
      setIsRecommending(false);
    }
  };

  if (loading) {
    return <div className="text-center mt-20 text-on-surface">Loading Concierge...</div>;
  }
  if (error) {
    return <div className="text-center mt-20 text-error">Error: {error}</div>;
  }

  return (
    <>
      {/* Header Section */}
      <section className="space-y-4">
        <h2 className="font-display-lg text-display-lg font-bold text-on-surface flex items-center gap-3">
          <span className="text-4xl">🍽️</span> AI-Powered Restaurant Recommender
        </h2>
        <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">
          Discover your next favorite meal based on your exact preferences, powered by AI. Let our premium concierge curate the perfect dining experience for you tonight.
        </p>
      </section>

      {/* Preferences Form (Elevated Glass Card) */}
      <section className="glass-panel rounded-xl p-6 md:p-8 relative overflow-hidden group">
        {/* Specular Highlight Top Edge */}
        <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-white/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <h3 className="font-headline-md text-headline-md font-semibold text-on-surface mb-6 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">tune</span> Perfect Your Search
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
          {/* Location */}
          <div className="space-y-2">
            <label className="font-label-caps text-label-caps text-on-surface-variant block">Location</label>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">location_on</span>
              <select 
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-lg text-on-surface pl-10 py-3 appearance-none focus:border-[#E23744] focus:ring-1 focus:ring-[#E23744] transition-all cursor-pointer">
                {filters?.locations.map((loc) => (
                  <option key={loc} className="bg-surface text-on-surface" value={loc}>{loc}</option>
                ))}
              </select>
              <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none">expand_more</span>
            </div>
          </div>
          {/* Budget */}
          <div className="space-y-2">
            <label className="font-label-caps text-label-caps text-on-surface-variant block">Budget</label>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">payments</span>
              <select 
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-lg text-on-surface pl-10 py-3 appearance-none focus:border-[#E23744] focus:ring-1 focus:ring-[#E23744] transition-all cursor-pointer">
                <option className="bg-surface text-on-surface" value="Any">Any Budget</option>
                <option className="bg-surface text-on-surface" value="Low">$$$ (Under ₹500)</option>
                <option className="bg-surface text-on-surface" value="Medium">$$$ (₹500 - ₹1500)</option>
                <option className="bg-surface text-on-surface" value="High">$$$ (₹1500+)</option>
              </select>
              <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none">expand_more</span>
            </div>
          </div>
          {/* Minimum Rating Slider */}
          <div className="space-y-2 md:col-span-2">
            <div className="flex justify-between items-end">
              <label className="font-label-caps text-label-caps text-on-surface-variant block">Minimum Rating</label>
              <span className="font-interactive-label text-interactive-label text-primary font-bold">{minRating.toFixed(1)}+ Stars</span>
            </div>
            <input 
              className="w-full h-2 bg-surface-container-highest rounded-lg appearance-none cursor-pointer accent-[#E23744]" 
              max="5" min="0" step="0.1" type="range" 
              value={minRating}
              onChange={(e) => setMinRating(parseFloat(e.target.value))}
            />
          </div>
          {/* Preferred Cuisines (Pills) */}
          <div className="space-y-3 md:col-span-2">
            <label className="font-label-caps text-label-caps text-on-surface-variant block">Preferred Cuisines</label>
            <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto custom-scrollbar pr-2">
              {filters?.cuisines.map((c) => {
                const isSelected = selectedCuisines.includes(c);
                return (
                  <button 
                    key={c}
                    onClick={() => toggleCuisine(c)}
                    className={`px-4 py-1.5 rounded-full border font-interactive-label text-sm transition-all ${
                      isSelected 
                        ? 'border-primary text-primary bg-primary/10 hover:bg-primary/20' 
                        : 'border-white/10 text-on-surface-variant bg-white/5 hover:border-white/30 hover:text-on-surface'
                    }`}
                    type="button"
                  >
                    {c}
                  </button>
                )
              })}
            </div>
          </div>
          {/* Additional Preferences */}
          <div className="space-y-2 md:col-span-2">
            <label className="font-label-caps text-label-caps text-on-surface-variant block">Additional Preferences (Vibe, Dietary, etc.)</label>
            <textarea 
              value={preferences}
              onChange={(e) => setPreferences(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-lg text-on-surface p-3 focus:border-[#E23744] focus:ring-1 focus:ring-[#E23744] transition-all resize-none" 
              placeholder="e.g., Romantic ambiance, rooftop seating, vegetarian options..." 
              rows={2}
            ></textarea>
          </div>
          {/* CTA */}
          <div className="md:col-span-2 pt-4">
            <button 
              onClick={getRecommendations}
              disabled={isRecommending}
              className="w-full btn-primary font-interactive-label text-interactive-label py-4 rounded-lg flex items-center justify-center gap-2 group relative overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed" 
              type="button"
            >
              <span className="relative z-10 flex items-center gap-2">
                <span className={`material-symbols-outlined ${isRecommending ? 'animate-spin' : 'animate-pulse'}`}>
                  {isRecommending ? 'sync' : 'auto_awesome'}
                </span>
                {isRecommending ? 'Curating Recommendations...' : 'Get Recommendations'}
              </span>
              {!isRecommending && <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>}
            </button>
          </div>
        </div>
      </section>

      {/* Results Section */}
      {recommendations.length > 0 && (
        <section className="space-y-6 pt-stack-md">
          <div className="flex justify-between items-end border-b border-white/10 pb-4">
            <h3 className="font-headline-md text-headline-md font-semibold text-on-surface">Curated Picks</h3>
            <span className="font-label-caps text-label-caps text-primary px-3 py-1 bg-primary/10 rounded-full border border-primary/20">{recommendations.length} Matches Found</span>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
            {/* Top Candidate */}
            {recommendations[0] && (
              <div className="lg:col-span-8 live-border rounded-xl p-[1px] group">
                <div className="glass-panel h-full rounded-xl overflow-hidden flex flex-col relative bg-surface-container/40 backdrop-blur-xl group-hover:bg-surface-container/60 transition-all duration-500">
                  <div className="p-6 md:p-8 flex flex-col justify-between flex-1 relative z-10">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-headline-md text-2xl font-bold text-white group-hover:text-primary transition-colors duration-300">
                          {recommendations[0].name}
                        </h4>
                        <div className="flex items-center gap-1 bg-white/5 backdrop-blur-sm px-3 py-1.5 rounded-lg text-primary font-bold border border-white/10 shadow-[0_0_10px_rgba(226,55,68,0.1)]">
                          <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>star</span> 
                          {recommendations[0].rating || 'N/A'}
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2 mb-4 font-label-caps text-label-caps">
                        <span className="text-on-surface-variant bg-white/5 px-2.5 py-1 rounded-md border border-white/5">
                          {recommendations[0].cost || 'Unknown'} Cost
                        </span>
                        <span className="text-on-surface-variant bg-white/5 px-2.5 py-1 rounded-md border border-white/5">
                          {recommendations[0].cuisines}
                        </span>
                      </div>
                    </div>
                    <div className="mt-8 bg-black/20 backdrop-blur-md border-l-2 border-primary p-4 rounded-r-lg shadow-[inset_4px_0_0_rgba(226,55,68,1)]">
                      <h5 className="font-interactive-label text-sm text-primary mb-1 flex items-center gap-1">
                        <span className="material-symbols-outlined text-[16px]">psychology</span> AI Match Reason
                      </h5>
                      <p className="text-sm text-on-surface-variant leading-relaxed">
                        {recommendations[0].explanation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Quick Compare list */}
            {recommendations.length > 1 && (
              <div className="lg:col-span-4 glass-panel rounded-xl p-6 flex flex-col">
                <h4 className="font-interactive-label text-lg font-bold text-on-surface mb-4">Quick Compare</h4>
                <div className="flex-1 space-y-4">
                  {recommendations.map((rec, i) => (
                    <div key={i} className="flex justify-between items-center pb-3 border-b border-white/10 last:border-0">
                      <div className="pr-2">
                        <p className="font-bold text-on-surface text-sm line-clamp-1">{rec.name}</p>
                        <p className="text-xs text-on-surface-variant line-clamp-1">{rec.cuisines}</p>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-primary text-sm font-bold">★ {rec.rating || 'N/A'}</p>
                        <p className="text-xs text-on-surface-variant">{rec.cost || 'Unknown'} Cost</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          {/* Secondary Candidates Grid */}
          {recommendations.length > 1 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter mt-gutter">
              {recommendations.slice(1).map((rec, i) => (
                <div key={i} className="glass-panel rounded-xl overflow-hidden group hover:glass-panel-active transition-all duration-300 bg-surface-container/20 cursor-pointer">
                  <div className="p-6 h-full flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-headline-md text-xl font-bold text-white group-hover:text-primary transition-colors">{rec.name}</h4>
                        <div className="flex items-center gap-1 text-primary font-bold">
                          <span className="material-symbols-outlined text-[16px]" style={{ fontVariationSettings: "'FILL' 1" }}>star</span> 
                          {rec.rating || 'N/A'}
                        </div>
                      </div>
                      <p className="text-xs text-on-surface-variant mb-4">{rec.cuisines}</p>
                      <p className="text-sm text-on-surface-variant line-clamp-3 mb-4 border-l-2 border-primary/50 pl-3">
                        {rec.explanation}
                      </p>
                    </div>
                    <div className="flex justify-between items-center mt-4 pt-4 border-t border-white/10">
                      <span className="font-label-caps text-label-caps text-on-surface-variant">{rec.cost || 'Unknown'} Cost</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}
    </>
  );
}
