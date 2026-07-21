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

---
*Note to Users: This roadmap is a living document. Priorities and versions are subject to change based on testing and feedback.*
