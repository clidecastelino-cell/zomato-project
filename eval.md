# Evaluation Framework (eval.md)

This document outlines the evaluation criteria and metrics for assessing the success and robustness of the AI-Powered Restaurant Recommendation System. The evaluation is mapped to the architectural components and the phase-wise implementation plan.

## 1. Data Ingestion & Preprocessing Evaluation (Phases 1 & 2)

**Objective:** Ensure the raw Zomato dataset is loaded reliably and transformed into a clean, usable state.

### Metrics & Checks:
- **Load Time & Caching:** Verify that `@st.cache_data` is functioning. The initial load may take a few seconds, but subsequent interactions must load the DataFrame instantly (< 100ms).
- **Data Integrity:** 
  - Zero `NaN` values in critical columns (`Restaurant Name`, `Location`, `Rating`, `Cost`, `Cuisine`) after preprocessing.
  - Cuisines are correctly parsed from comma-separated strings into usable lists or standardized strings.
- **Fail-safes:** Verify that if the Hugging Face API is unreachable, the application catches the error gracefully rather than crashing.

## 2. Integration & Filtering Logic Evaluation (Phase 4)

**Objective:** Ensure the Pandas filtering logic strictly enforces hard user constraints before hitting the LLM.

### Metrics & Checks:
- **Constraint Accuracy:** 
  - If a user selects "Bangalore", all outputted candidates MUST have their location mapped to Bangalore.
  - If a user selects a Minimum Rating of 4.5, all candidates MUST have a rating >= 4.5.
- **Empty State Handling:** When overly restrictive constraints yield 0 results, the system must detect this and display a user-friendly message rather than passing an empty list to the LLM.
- **Token Optimization (Top N Extraction):** The system must successfully truncate results (e.g., to the Top 15) to prevent exceeding the Gemini API context window.

## 3. LLM Engine Evaluation (Phase 5)

**Objective:** Assess the quality, formatting, and grounding of the AI-generated recommendations.

### Metrics & Checks:
- **No Hallucinations (Grounding):** 100% of the restaurants recommended by the LLM MUST exist in the candidate list provided by the Integration Layer. The LLM must not invent restaurants.
- **Schema Adherence:** The LLM must return the output in the exact requested format (e.g., JSON). Track the success rate of the UI parser against the LLM output.
- **Explanation Quality (Personalization):** 
  - The AI-generated explanations should specifically reference the user's "Additional Preferences" (e.g., if the user asks for a "romantic date spot," the explanation should highlight ambiance rather than just restating the menu).
- **Graceful Degradation:** If the user enters nonsensical text in the preferences box, the LLM should ignore the noise and default to highlighting the best restaurants based on the structured data.

## 4. UI/UX & End-to-End Evaluation (Phases 3 & 6)

**Objective:** Ensure a seamless and intuitive user experience.

### Metrics & Checks:
- **API Key Security:** The API key input must obscure text (password mode) and must not be logged to the console.
- **Responsiveness:** The UI should update cleanly without unnecessary page reloads.
- **Error Handling:** 
  - Invalid API keys must trigger a specific, actionable error message.
  - Network timeouts with the Gemini API must be caught and displayed gracefully.
- **Visual Presentation:** The final restaurant cards should clearly display the name, rating, cost, and the AI explanation without Markdown rendering bugs.

## 5. Summary of Automated Testing Opportunities

To automate this evaluation in the future, the following tests could be implemented:
1. **Unit Tests:** For the Pandas filtering functions to ensure constraint accuracy.
2. **Integration Tests:** Passing mock filtered lists to the LLM and asserting that the output parses correctly as JSON.
3. **LLM Eval (LLM-as-a-Judge):** Running a batch of test user inputs and using another LLM to score whether the generated explanations successfully addressed the implicit preferences.
