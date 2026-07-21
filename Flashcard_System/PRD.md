# Product Requirements Document (PRD)

## 1. Executive Summary & Product Overview
**Product Name:** Spaced Repetition Flashcard System
**Problem Statement:** Traditional studying relies on inefficient rote memorization. Existing Spaced Repetition Systems (SRS) like Anki have steep learning curves, outdated UIs, and lack modern LLM integration to automate the grueling process of flashcard creation.
**Target Audience:** Students, self-learners, and professionals seeking a highly optimized, automated study system.
**Core Value Proposition:** A modern, self-hosted web application that leverages the Ebbinghaus Forgetting Curve for optimal memory retention, while utilizing the Gemini API to instantly generate perfect flashcards from unstructured textbook data or notes.
**Success Metrics:** Users can ingest 10 pages of notes and generate 50 flashcards via the LLM pipeline in under 20 seconds. The algorithmic scheduler successfully filters daily reviews based on interval progression and failure state resets.
**Out of Scope:** Native mobile application deployment (iOS/Android wrappers), public deck-sharing marketplace.

## 2. Tech Stack & Architecture
**User Interface / Trigger:** React (Next.js) web application with strict CSS Media Queries for responsive mobile-browser usage.
**Backend / Database:** Python (FastAPI) server connected to a PostgreSQL database.
**APIs & Integrations:** 
- **Google Gemini API:** For LLM text ingestion (extracting concepts into JSON flashcard schemas).
**Infrastructure:** 
- **Homelab Deployment:** Wrapped in `docker-compose` specifically architected for local server deployment (e.g., Unraid, Proxmox). 
- **Remote Access:** Designed to be accessed globally via a private mesh VPN (Tailscale/WireGuard), circumventing the need for public SSL or complex web authentication.
**Data Privacy & Configuration:** `.env` standard for securing the Gemini API keys locally.

## 3. Core Features & Requirements
- **Feature 1: The Spaced Repetition Engine (SRS)** 
  - An algorithmic backend utilizing the industry-standard **SuperMemo-2 (SM-2)** algorithm.
  - Tracks the interval stage, ease factor, and repetition count of every flashcard.
  - Successful recall pushes the interval exponentially based on the dynamic ease factor.
  - Failed recall resets the repetition count and adjusts the ease factor to force more frequent reviews.
- **Feature 2: Shared-Deck Relational Database Schema**
  - `Users` Table: Stores basic profile names for members of the household.
  - `Decks` Table: Global folders that group cards by subject. Includes an `Owner_ID` (Foreign Key to `Users`) to strictly prevent non-owners from editing or deleting a shared deck.
  - `Cards` Table: Stores the static front/back text and the foreign key to the Deck.
  - `User_Card_Progress` Table (The SM-2 Engine): A mapping table linking a `User_ID` to a `Card_ID`. This isolates the algorithmic math (Next_Review_Date, Interval, Ease_Factor), allowing multiple users to study the exact same cards while maintaining perfectly independent learning intervals.
  - `Review_Logs` Table: A historical ledger tracking every card flip and grade to generate user-specific retention statistics.
- **Feature 3: Multi-Modal Ingestion Pipeline**
  - *Manual Entry:* Standard UI for single-card creation.
  - *Bulk CSV:* Parses user-uploaded `.csv` files for mass legacy imports.
  - *LLM Generator (Transcripts & Text):* Sends raw pasted study notes or massive lecture transcripts to the Gemini API and parses the returned JSON.
  - *LLM Generator (Word & PDF):* Uses backend libraries (`python-docx`) to strip text from Word files, and leverages the Gemini File API's native multi-modal capabilities to directly ingest and parse scanned PDF textbooks into flashcards.
- **Feature 4: The Daily Triage UI**
  - A clean, distraction-free study interface that queries the backend for *only* the cards whose interval has expired today.
- **Feature 5: Netflix-Style Profile Selector**
  - Upon loading the web app via the homelab IP, users are presented with a frictionless profile selection screen (e.g., "Who's studying?").
  - This dictates session state, ensuring a user only sees their specific decks and prevents algorithmic cross-contamination.
- **Feature 6: Automated Git Version-Control Backups**
  - A backend cron job runs nightly, extracting the database state and dumping it into modular `.json` files.
  - The script executes an automated `git push` to a private GitHub repository, providing flawless, bloat-free version control and time-travel rollback capabilities for all flashcard data.
