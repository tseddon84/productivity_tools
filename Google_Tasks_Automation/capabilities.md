# Google Tasks Productivity Automations

This tool is a custom Google Apps Script designed to run inside your Google Workspace. It connects a Google Sheet (acting as a database) to your Google Tasks and Google Calendar.

## Core Capabilities

1. **The Master Hub Integration:** 
   - Uses a Google Sheet with 3 main tabs: `Recurring Habits`, `Project Backlog`, and `Household Cleaning Queue`.
   - Automatically maps categories in your spreadsheet to specific Task Lists on your phone.

2. **Daily Briefing Generation:**
   - Runs automatically at 4:00 AM every day.
   - Pushes tasks to your Google Tasks app.
   - Compiles a clean text summary of your day and pushes it to a daily Calendar event (which is natively read out by the Google Assistant "Good Morning" routine on Pixel devices).

3. **The "Circuit Breaker" (Dynamic Task Limiting):**
   - Automatically scans your active Task Lists before generating new tasks.
   - Enforces a strict limit of **3 open tasks per category**. If a list is full, it safely skips generating new tasks to prevent "task bankruptcy" and overwhelm.

4. **Specific Day Scheduling:**
   - Allows exact day scheduling for recurring habits. You can type "Daily", "Monday", "Tuesday", etc. into the spreadsheet, and the script will drop the task perfectly on schedule.

5. **Household Priority Rotation:**
   - Reads your household cleaning chores, identifies the single highest-priority chore, pushes it to your tasks, and automatically rotates it to the bottom of the spreadsheet so you only get 1 deep clean chore a day.

6. **Respawn Suppression:**
   - Prevents one-off Project Tasks from respawning daily if you completed them on your watch but haven't updated the spreadsheet yet. It queries your recently completed tasks (last 7 days) and suppresses duplicates.

7. **Weekly Progress Metrics (Sunday Review):**
   - Runs automatically at 6:00 AM on Sundays.
   - Calculates your habit adherence over the last 7 days (e.g., "Daily Step Goal: 4/7 completions").
   - Scrapes your Google Tasks Inbox for any unorganized voice notes you took throughout the week.
   - Compiles this data into a Sunday Calendar Event for you to easily review over coffee with Gemini.
