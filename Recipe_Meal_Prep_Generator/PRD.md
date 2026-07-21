# Product Requirements Document (PRD)

## 1. Executive Summary & Product Overview
**Product Name:** Recipe & Meal Prep Generator
**Problem Statement:** Meal planning, macro tracking, and grocery list aggregation are tedious manual processes. Existing recipe apps either lock users into walled gardens, fail to normalize ingredients (breaking grocery lists), or lack automated calendar integration.
**Target Audience:** Power-users looking for a self-hosted, offline-first, highly accurate meal planner and grocery aggregator.
**Core Value Proposition:** A Dockerized, personal cookbook that ingests messy recipe data via LLM parsing or external APIs, normalizes all ingredients into a strict dictionary, and automates weekly meal scheduling, macro tracking, and grocery list generation.
**Success Metrics:** Users can import a messy food blog post in under 10 seconds, generate a perfectly aggregated weekly grocery list with zero duplicate items, and automatically push the 7-day meal plan to Google Calendar.
**Out of Scope:** Mobile application development (this is a responsive web app), social sharing features, and real-time grocery delivery API integrations (e.g., Instacart) are out of scope for v1.0.

## 2. Tech Stack & Architecture
**User Interface / Trigger:** React (Next.js) web application (or Python Dash/Streamlit if preferred).
**Backend / Database:** Python (FastAPI or Flask) server connected to a PostgreSQL database.
**APIs & Integrations:** 
- **Google Gemini API:** For raw text parsing and nutritional estimation.
- **Spoonacular API:** For spontaneous recipe discovery (built with an adapter pattern).
- **Google Calendar API:** For scheduling meal reminders via OAuth2.
**Infrastructure:** Entirely wrapped in `docker-compose` for 1-click local deployment.
**Data Privacy & Configuration:** Hosted locally. All API keys and OAuth credentials will be securely managed via a `.env` file, ensuring the repository remains safe to share or clone.

## 3. Core Features & Requirements
- **Feature 1: Multi-Modal Recipe Ingestion Engine** 
  - *LLM Text Parser:* Accepts raw, copied/pasted text from blogs, sends it to the free Gemini API, and normalizes it into strict JSON (including estimated macros per serving).
  - *Direct JSON Upload:* Accepts pre-formatted `.json` files.
  - *Spoonacular API Integration:* A discovery search bar that fetches random recipes. The codebase must use a "Provider Interface" so Edamam or other APIs can be easily swapped in later without rewriting the core parsing logic.
- **Feature 2: The Normalized Ingredient Dictionary**
  - All incoming recipes have their ingredients stripped and matched against a central database table. 
  - Ensures accurate macro calculation and prevents "1 cup rice" and "100g rice" from remaining separate entities.
- **Feature 3: The Generation & Scheduling Engine**
  - Users input caloric constraints, dietary restrictions, and select days (e.g., "Plan 5 dinners").
  - The algorithm randomly selects compliant meals from the local database and presents them for user confirmation.
  - Upon confirmation, the app pushes the meals as events to Google Calendar.
- **Feature 4: The Grocery Aggregator**
  - Iterates over the scheduled meals, cross-references the Ingredient Dictionary, runs unit-conversion math, and outputs a highly condensed, mathematically perfect grocery list.
- **Feature 5: Portable Configuration & Documentation**
  - The project must include a `secrets.template.env` file.
  - Comprehensive documentation must be written detailing exactly how a new user can clone the project, obtain their own Google Cloud OAuth credentials and Gemini API keys, insert them into their local `.env`, and launch the Docker container.

---

## 4. Unresolved Ambiguities & Open Questions (User Review Required)

**1. Tech Stack Confirmation:** 
- **Resolved:** Backend will be built in Python (FastAPI/Flask) to leverage your existing knowledge. Database is confirmed as PostgreSQL. 

**2. Calendar Integration & Portability:**
- **Resolved:** We will use Google Calendar API. The project will strictly enforce a `.env` based configuration model and include step-by-step setup documentation for obtaining OAuth credentials so the project can be seamlessly cloned and deployed by others.
