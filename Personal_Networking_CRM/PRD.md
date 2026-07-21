# Product Requirements Document (PRD)

## 1. Executive Summary & Product Overview
**Product Name:** Personal Networking CRM
**Problem Statement:** Maintaining weak-tie relationships (mentors, former colleagues, alumni) is cognitively draining. Because humans forget to maintain contact during peaceful periods, reaching out only when a favor is needed feels transactional and damaging to the relationship's social capital.
**Target Audience:** Professionals and individuals looking to systematically maintain their social and professional networks with high emotional intelligence and zero friction.
**Core Value Proposition:** A "headless" CRM that uses Notion's world-class mobile UI for frictionless data entry, paired with a lightweight Python homelab script that algorithmically calculates interaction intervals and pushes proactive contact reminders.
**Success Metrics:** The system successfully identifies contacts who have breached their tier-based time intervals and successfully delivers a readable notification payload containing their last known rich-text notes.
**Out of Scope:** Automated messaging (the system will remind the user to text/email, but will not send the message on their behalf).

## 2. Tech Stack & Architecture
**User Interface & Database:** Notion (Free Personal Tier) accessed via the Notion API.
**Compute Engine:** Python script running in a Docker container on the user's local homelab.
**Trigger Mechanism:** Local homelab `cron` job set to execute once daily at 8:00 AM.
**Security:** `.env` file securing the Notion Integration Token and Webhook URLs on the local homelab. 

## 3. Core Features & Requirements
- **Feature 1: The Notion "Dumb Terminal" UI**
  - A strictly structured Notion database containing: `Name`, `Tier`, `Last_Contacted_Date`, `Rich_Text_Notes`, and a boolean checkbox: `I_Contacted_Them_Today`.
  - Serves as the frictionless mobile and desktop interface for updating contact details post-interaction.
- **Feature 2: The Interval Algorithm (Python Engine)**
  - The script executes a daily `GET` request to the Notion API.
  - **The Reset Trigger:** If it detects the `I_Contacted_Them_Today` checkbox is marked `true`, it issues a `PATCH` request to update the `Last_Contacted_Date` to today's date, and instantly unchecks the box.
  - It maps the `Tier` variable to mathematical integers (e.g., Mentor = 90 days).
  - It calculates the `delta` between `Last_Contacted_Date` and `Current_Date`.
  - If `delta > Tier_Interval`, the contact is flagged as `Overdue`.
- **Feature 3: The Notification Payload**
  - For all `Overdue` contacts, the script extracts the `Name` and the last recorded `Rich_Text_Notes`.
  - It compiles this into a clean payload (e.g., *"Action Required: Text [Name]. It has been 92 days. Last known note: [Notes]"*).
  - The payload is POSTed to the user's preferred notification engine.

---

## Proposed Scaffolding Code Changes
If this blueprint is approved, I will execute the following commands on our `project_planning` branch:
1. Create directory `Personal_Networking_CRM/`.
2. Write this exact Tech Spec into `Personal_Networking_CRM/PRD.md`.
3. Create the AI-tracking log `.agents/copyright_logs/personal_networking_crm.md`.

---

## 4. Unresolved Ambiguities & Open Questions (User Review Required)

**1. The Notification Engine:** 
- **Resolved:** The Python script will support a dual-engine output: **Discord Webhooks** (for immediate push notifications) and **Automated Email via SMTP** (to seamlessly feed downstream automations like the Task Tracker). The user can toggle one or both via the `.env` file. Telegram support has been explicitly cut to prevent unnecessary dependency bloat.

**2. The "Contacted" Reset Trigger:**
- **Resolved:** We will use the **"I Contacted Them Today" Checkbox**. This is a superior UX design. The user never has to fiddle with Notion's clunky date-picker on their phone. They simply tap the checkbox. When the Python script runs its daily cron job, it will scan for checked boxes, programmatically overwrite the `Last_Contacted_Date` to the current date via the Notion API, and then uncheck the box to reset the cycle.
