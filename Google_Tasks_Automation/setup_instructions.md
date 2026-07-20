# Setup Instructions: Google Tasks Productivity Automations

Follow these steps exactly to implement the automated productivity script in your Google Account.

## Step 1: Create the Master Hub (Google Sheet)
1. Go to Google Drive and create a brand new Google Sheet. 
2. At the bottom of the screen, double-click the default "Sheet1" tab to rename it. 
3. You MUST create exactly 3 tabs, spelled exactly like this (case sensitive, no extra spaces):
   - `Recurring Habits`
   - `Project Backlog`
   - `Household Cleaning Queue`

### Formatting the Tabs
Set up the top row of each tab with the following headers:

**Tab 1: Recurring Habits**
- Column A: Category
- Column B: Goal Name
- Column C: Frequency *(Accepts: Daily, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)*
- Column D: Target Metric
- Column E: Metric Type
- Column F: Is Active? *(Must be a Checkbox, or TRUE/FALSE)*

**Tab 2: Project Backlog**
- Column A: Category
- Column B: Project
- Column C: Task Name
- Column D: Status *(Script specifically looks for "Next Action")*
- Column E: Priority
- Column F: Notes

**Tab 3: Household Cleaning Queue**
- Column A: Area
- Column B: Priority *(Numbers)*
- Column C: Urgent Issue?
- Column D: Last Cleaned Date

## Step 2: Add the Code
1. While still inside your Google Sheet, click **Extensions** in the top menu, then click **Apps Script**.
2. A new tab will open with a code editor. Delete all the default code (`function myFunction() { ... }`).
3. Paste the entire `ProductivityAutomations.gs` code into this window.
4. Click the **Save** icon (looks like a floppy disk) at the top.

## Step 3: Enable the Required APIs
This script requires permission to talk to your Google Tasks and Google Calendar.
1. In the Apps Script editor, look at the far left menu and click the **Services** icon (it looks like a `+` next to the word Services).
2. Scroll down the list and select **Google Calendar API**. Click **Add**.
3. Click the **+** next to Services again.
4. Scroll down and select **Google Tasks API**. Click **Add**.

## Step 4: Authorize and Start the Engine
1. At the top of the Apps Script editor, there is a dropdown menu (likely says `setupTriggers`). Make sure it is set to `setupTriggers`.
2. Click the **Run** button next to it.
3. A scary warning box will pop up saying "Authorization Required". Click **Review permissions**.
4. Choose your Google account.
5. Google will say "Google hasn't verified this app". Click **Advanced** at the bottom, then click **Go to Untitled project (unsafe)**.
6. Click **Allow** to give the script permission to manage your tasks and calendar.

## Step 5: Test It!
1. Add some test data to your Google Sheet (e.g., check the box for a Daily habit, and mark a project task as "Next Action").
2. In the Apps Script editor, change the top dropdown from `setupTriggers` to `generateDailyTasks`.
3. Click **Run**.
4. Check your Google Tasks and Google Calendar—your tasks will be there! From now on, it will run automatically every day at 4:00 AM.

---

## Code Backups & Rollbacks
Because Google Apps Script does not natively save historical versions of your code easily, it is highly recommended to keep a local backup.
- Before pasting a major update (e.g., moving from v1.0.0 to v2.0.0), create a text file on your computer named `ProductivityAutomations_v1.0.0.gs` and paste the working code into it.
- If a new update breaks your workflow, simply open your backup file, copy the old code, and paste it back into the Apps Script editor to safely roll back.
- Always check the `CHANGELOG.md` file before updating to see if the new version requires a **[MIGRATION]** (which means you need to add or rename columns in your Google Sheet).
