# Product Roadmap: Personal Networking CRM

**Vision Statement:** A frictionless, mobile-optimized networking CRM built on Notion that automates relationship tracking and intelligent outreach reminders without requiring manual data entry maintenance.

## Phase 1: V1 Core Engine (Current Focus)
**Status:** ✅ Completed | **Target Version:** v0.1.0
*User Value:* Eliminates the mental load of remembering to reach out to contacts by fully automating interval-based outreach math and pushing notifications directly to email and Discord.
- [x] Notion API integration for fetching and parsing contact intervals.
- [x] Automated daily processing via Docker scheduling (03:30 AM).
- [x] Discord and Email automated notifications for overdue contacts.
- [x] Frictionless mobile-optimized Notion UI workflow (1-tap logging).

## Phase 2: Database Schema Expansion (Up Next)
**Status:** 📅 Planned | **Target Version:** v0.2.0
*User Value:* Allows for granular memory tracking, relationship context, and advanced filtering to make automated outreach feel incredibly personal and authentic.
- [ ] **Milestone 1: Create Dedicated Notion Properties**
  - [ ] Birthday
  - [ ] Spouse (Name)
  - [ ] Spouse's Birthday
  - [ ] Kids (Names/Ages)
  - [ ] Kids' Birthdays
  - [ ] Pets
  - [ ] Likes
  - [ ] Dislikes
  - [ ] Shared Activities
  - [ ] Preferred Method of Contact
  - [ ] Contact Information
  - [ ] Occupation
  - [ ] Company
- [ ] **Milestone 2: Notification Engine Upgrade**
  - Update `notion_service.py` to parse the new structured fields.
  - Inject the context variables directly into the automated morning outreach summaries.

## Phase 3: Advanced Intelligence (Ideation)
**Status:** 💡 Ideation | **Target Version:** TBD
*User Value:* Transforms the tool from a reminder script into a proactive relationship manager.
- [ ] **Location-Based Triaging ("I'm in Town"):** Add a travel trigger that scans the database by City/State and instantly emails a sorted list of local contacts when you travel.
- [ ] **LLM Context Summarization:** Pass historical interaction notes through a lightweight AI model to generate a perfect 2-sentence relationship summary and icebreaker for the morning email.
- [ ] **Automated "Dormant" Tagging:** If a contact's interval is ignored for 3 consecutive cycles, automatically tag them as `Dormant` to keep the active database clean and prevent bloat.
- [ ] **Life Event Auto-Triggers:** Force contacts to the top of the morning priority list if the script detects that today matches a birthday or anniversary field.

---
*Note to Users: This roadmap is a living document. Priorities and versions are subject to change based on testing and feedback.*
