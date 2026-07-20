# The Google Ecosystem Productivity Protocol (V2)

## Phase 1: High-Level Structure (The Master Hub)
**Tool:** Google Sheets (One file, 3 Core Tabs)
The spreadsheet acts as the "Master Database" for your entire life's productivity, built on a strict schema.

**The 3 Tabs:**
1. **Recurring Habits:** Tracks your daily and specific-day habits (e.g., Fitness, WGU, Coding practice). The script uses exact days (Monday, Tuesday, Daily) to push these tasks.
2. **Project Backlog:** Tracks one-off tasks mapped to specific projects. Tasks are only pushed to your watch when you mark them as "Next Action" here.
3. **Household Cleaning Queue:** A stack-ranked list of chores. The system automatically pulls the single highest-priority chore, assigns it to you, and drops its priority to the bottom to prevent chore overload.

## Phase 2: Automated Daily Execution (The Automation Engine)
**Tools:** Google Apps Script, Google Tasks (App & Pixel Watch), Google Calendar

**The Morning Briefing (4:00 AM Daily Run):**
- **Action:** The Apps Script automatically scans your Google Sheet.
- **Circuit Breaker Check:** The script queries your Google Tasks. If any category has 3 or more open tasks, it skips generating new ones for that list to prevent "Task Bankruptcy."
- **Respawn Suppression:** The script ensures that one-off Project Tasks you completed recently do not respawn, even if you forgot to update the Master Hub.
- **Output:** Tasks are assigned directly to your wrist via Google Tasks on your Pixel Watch. A summary is written to a "Daily Briefing" Google Calendar event so your Google Assistant "Good Morning" routine can read it to you.

## Phase 3: Frictionless Capture (The Inbox)
**Tools:** Google Assistant, Google Tasks ("@default" list)

**The Capture Flow:**
- Throughout the week, whenever an idea, to-do, or chore pops into your head, you use your Pixel Watch or Phone.
- **Action:** *"Hey Google, add a task to vacuum the car."*
- **Routing:** Google automatically drops this into your default Google Tasks list.
- **Why this works:** It requires zero manual data entry in the moment, keeping you in flow. 

## Phase 4: The Sunday Review (Rigor Enforcement)
**Schedule:** Every Sunday morning at 6:00 AM.
**Tools:** Google Apps Script, Google Calendar, Gemini

**The Review Automation:**
1. **Data Aggregation:** The Apps Script runs automatically and queries the Google Tasks API.
2. **Weekly Metrics:** It calculates exactly how many times you completed specific habits over the last 7 days (e.g., *"Daily Step Goal: 4/7 completions"*).
3. **Inbox Scraping:** It pulls all the unorganized voice notes you captured throughout the week from your default Tasks list.
4. **Calendar Injection:** It injects this entire data report into a "SUNDAY REVIEW PREP" calendar event.

**Your Manual Action:**
Sit down with your coffee, copy the data from the calendar event, and paste it into Gemini with this prompt:
> *"Help me review this data. Here is what I captured in my inbox, and here are my habit metrics for the week. What bottlenecks caused me to miss my habits, and what metrics do I need to update in my Google Sheet?"*

After reviewing with Gemini, you manually update the Master Hub spreadsheet to lock in your progress and set your targets for the new week.
