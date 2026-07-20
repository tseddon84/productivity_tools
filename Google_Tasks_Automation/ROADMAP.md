# Product Roadmap: Google Tasks Automation

**Vision Statement:** Transform a passive task generator into an active, schedule-aware, context-sensitive productivity engine without compromising the integrity of the Master Hub database.

---

## Phase 1: The Schema Split (Household vs. Chores)
**Status:** 🚧 In Progress | **Target Version:** v1.1.0
*User Value:* Separates finite, mandatory maintenance (Household) from endlessly recurring tasks (Chores) so one-time repairs aren't accidentally reassigned months later.
- [ ] **Milestone 1:** Add a new `Chores Queue` tab to the Master Hub spreadsheet.
- [ ] **Milestone 2:** Update Google Apps Script parsing arrays to handle the new tab logic.
- [ ] **Milestone 3:** Ensure "Household" tasks are pulled once and never receive a priority rotation bump.

## Phase 2: End-of-Day Forgiveness (The Graveyard)
**Status:** 📅 Planned | **Target Version:** v1.2.0
*User Value:* Provides a psychological clean slate every morning by wiping yesterday's failed habits, while securely archiving them so Sunday Review failure metrics remain perfectly accurate.
- [ ] **Milestone 1:** Create an automated `[Archive] Skipped Tasks` hidden list.
- [ ] **Milestone 2:** Build a 11:55 PM trigger sweep targeting only "Recurring Habits" and "Chores Queue".

## Phase 3: Webhook Notifications (Google Chat)
**Status:** 📅 Planned | **Target Version:** v1.3.0
*User Value:* Bypasses passive smartwatch checking to deliver a hard, unmissable ping to your phone when you are falling critically behind on a specific list.
- [ ] **Milestone 1:** Implement secure `PropertiesService` storage for the Google Chat Webhook URL.
- [ ] **Milestone 2:** Add `UrlFetchApp` logic to fire when a `CIRCUIT_BREAKER` trip condition is met.

## Phase 4: Task Urgency Escalation (Deadlines)
**Status:** 📅 Planned | **Target Version:** v1.4.0
*User Value:* Ensures critical project work is never buried beneath routine chores as deadlines approach.
- [ ] **Milestone 1:** Add a `Deadline` column (Index 6) to the Project Backlog schema.
- [ ] **Milestone 2:** Update 4:00 AM script to calculate Date math and force `[URGENT]` prepend for tasks within 3 days.

## Phase 5: Pomodoro Time-Blocking (Calendar Sync)
**Status:** 💡 Ideation | **Target Version:** v1.5.0
*User Value:* Actively blocks out guaranteed time on your calendar to accomplish generated tasks, preventing you from overcommitting your day.
- [ ] **Milestone 1:** Add an `Estimated Minutes` column (Index 7) to the Master Hub schema.
- [ ] **Milestone 2:** Integrate Google Calendar Advanced Service to query free/busy slots on the "Tasks" calendar.
- [ ] **Milestone 3:** Generate distinct calendar events for assigned tasks based on duration.

---
*Note to Users: This roadmap is a living document. Priorities and versions are subject to change based on testing and feedback.*
