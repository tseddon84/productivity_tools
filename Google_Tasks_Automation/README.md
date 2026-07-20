# 🚀 Google Tasks Productivity Automation Engine

![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
![Google Tasks](https://img.shields.io/badge/Google%20Tasks-4285F4?style=for-the-badge&logo=google-tasks&logoColor=white)
![Google Apps Script](https://img.shields.io/badge/Apps%20Script-0F9D58?style=for-the-badge&logo=google&logoColor=white)
![Version](https://img.shields.io/badge/version-v1.0.0-blue?style=for-the-badge)

A robust, serverless productivity system that transforms a Google Sheet into an automated "Master Hub." It seamlessly bridges your static goals and projects into actionable, daily tasks pushed directly to your Google Tasks inbox and Pixel Watch.

> 📖 **Read the [CHANGELOG.md](./CHANGELOG.md)** for a history of updates, features, and migration warnings.

---

## ✨ Features

- 🧠 **Dynamic Circuit Breakers:** Automatically prevents "Task Bankruptcy." If a specific category (e.g., Household) already has 3 uncompleted tasks, the script halts generation for that list until you catch up.
- 📅 **Specific Day Scheduling:** Drop habits exactly when you need them. Type `Daily`, `Monday`, or `Friday` into your spreadsheet, and the script maps it dynamically.
- 🔄 **Stack-Ranked Chores:** Reads a queue of household chores, pops the single highest priority item to your tasks, and rotates it to the bottom of the list to prevent chore overload.
- 🛡️ **Respawn Suppression:** Completed a project task on your watch but forgot to update the spreadsheet? The script scans your recently completed tasks (last 7 days) and suppresses duplicates from respawning.
- 📊 **Automated Sunday Review:** Automatically aggregates your habit adherence for the last 7 days (e.g., *Daily Step Goal: 4/7 completions*) and scrapes your default inbox for unorganized voice notes, injecting a clean report directly into a Sunday Calendar Event.
- 🎙️ **Frictionless Voice Capture:** Say *"Hey Google, add a task..."* to your phone or watch. It lands in your default inbox, ready to be processed during your Sunday Review.

---

## 🏗️ Architecture

The system operates entirely within the Google Workspace ecosystem using Google Apps Script (JavaScript). 

1. **Master Hub (Google Sheets):** The source of truth. Contains strict schemas for Habits, Projects, and Chores.
2. **Automation Engine (Apps Script):** Contains two time-driven triggers:
   - `generateDailyTasks`: Runs at 4:00 AM daily to sync tasks.
   - `generateSundayReview`: Runs at 6:00 AM on Sundays to aggregate weekly metrics.
3. **Execution Hub (Google Tasks & Calendar):** The front-end where the user actually interacts with the tasks, easily accessible via Wear OS.

---

## 🚀 Installation & Setup

### 1. Create the Database
Create a new Google Sheet with exactly three tabs:
- `Recurring Habits`
- `Project Backlog`
- `Household Cleaning Queue`

### 2. Deploy the Code
1. In your Google Sheet, click **Extensions > Apps Script**.
2. Delete the default code and paste the contents of `ProductivityAutomations.gs`.
3. Click the **Services** (`+`) button on the left sidebar. Add both the **Google Tasks API** and **Google Calendar API**.

### 3. Initialize the Engine
1. Select `setupTriggers` from the top dropdown menu and click **Run**.
2. Accept the Google security prompts to authorize the script.
3. The script will automatically bind itself to your account and run every morning at 4:00 AM!

---

## 🛠️ Usage Workflow

1. **Daily:** Wake up. Your Pixel's "Good Morning" routine will read your Daily Briefing calendar event. Check off tasks on your watch as you complete them.
2. **Ad-hoc:** Use Google Assistant voice capture to dump thoughts into your default Tasks inbox.
3. **Weekly:** Every Sunday morning, sit down with the automated Calendar report. Paste the report into Gemini to analyze your bottlenecks, then update your Master Hub spreadsheet to lock in the next week's goals.
