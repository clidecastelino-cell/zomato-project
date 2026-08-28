# Phase-Wise Implementation Plan

This document outlines the step-by-step phases to build the AI-Powered Restaurant Recommendation System, migrating from the initial Streamlit prototype to a robust Next.js frontend with a Python backend, adhering to the Lumina Gastronomy design system.

## Phase 1: Environment Setup & Architecture Initialization
**Goal:** Establish a decoupled architecture with a Next.js frontend and a Python (FastAPI) backend.
- **Backend:** Set up a Python virtual environment. Create `requirements.txt` with `fastapi`, `uvicorn`, `pandas`, `datasets`, `groq`. Initialize `main.py` as the API entry point.
- **Frontend:** Initialize a Next.js (App Router) project with Tailwind CSS and Framer Motion for animations.
- **Design Tokens:** Translate `DESIGN.md` into `tailwind.config.ts` (mapping colors like `#0b1326` to `background`, `#E23744` to `primary`, and configuring Outfit/Inter fonts).

## Phase 2: Data Ingestion & API Layer (Backend) - [IN PROGRESS]
**Goal:** Expose the Zomato dataset and AI logic via RESTful endpoints.
- Port existing Pandas data cleaning from `app.py` into a robust data loader in the backend.
- Create an endpoint `POST /api/recommend` that accepts user preferences (Location, Budget, Rating, Cuisines, Additional Prefs).
- Implement the filtering logic within the FastAPI endpoint.
- Integrate the Groq LLM call in the backend to return structured JSON recommendations.

## Phase 3: Frontend Foundation & UI Skeleton
**Goal:** Build the Lumina Gastronomy base layout.
- Create the global layout with the deep navy background (`#0b1326`), applying the Fluid-Fixed Hybrid grid.
- Build the Glassmorphic Sidebar (fixed 280px on desktop) for settings, navigation, and API key input.
- Set up typography using `next/font` for Outfit (display/interactive) and Inter (body).

## Phase 4: User Input Components (Frontend)
**Goal:** Create high-fidelity, interactive input elements for user preferences.
- Build the preferences form using glassmorphic cards (Level 1 Elevation: `white/5` fill, `white/10` border, 12px blur).
- Implement custom form controls:
  - Location Dropdown & Budget Selector.
  - Cuisine Multiselect with pill-shaped chips.
  - Interactive Rating Slider.
- Build the Primary Call-to-Action button (Crimson `#E23744`, inner top-light, hover glow).

## Phase 5: Recommendation Engine Integration
**Goal:** Connect the frontend to the FastAPI backend.
- Implement API fetching logic in Next.js (using `fetch` or SWR/React Query).
- Handle loading states with a premium food-related spinner or staggered skeleton loaders.
- Securely pass the Groq API key from frontend state to the backend (via headers).

## Phase 6: Output Display & Polish (Lumina Gastronomy Aesthetics)
**Goal:** Render the AI recommendations beautifully with depth and micro-animations.
- **Restaurant Cards:** Build the Level 2 Elevation cards with background imagery and dark gradient overlays.
- **AI Highlight:** Implement the "Live Border" gradient stroke for the top AI-curated picks.
- Display the AI's explanation with clear typography and subtle emphasis.
- Refine responsive behaviors (single column on mobile) and add Framer Motion stagger-fade-in effects for the results.
