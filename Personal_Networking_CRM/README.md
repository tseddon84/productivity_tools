# Personal Networking CRM

A lightweight, "headless" CRM that uses Notion for a beautiful mobile UI, and a Python Docker container to perform automated interval math and push notifications via Discord or Email.

## Features
- **Frictionless UI:** Use the Notion mobile app to log coffee chats in 5 seconds.
- **The "Contacted Today" Reset:** Simply check a box in Notion when you text someone. The script will automatically update the date and uncheck the box for you.
- **Dual-Engine Notifications:** Sends a daily payload of "overdue" contacts to your Discord Webhook, or your Email inbox (designed to feed your Task Tracker).

## Setup Instructions

### 1. Build the Notion Database
Create a new database in Notion with the following EXACT columns (case-sensitive):
- `Name` (Title property)
- `Tier` (Select property: Options MUST include `Inner Circle`, `Mentor`, `Colleague`, `Acquaintance`, `Alumni`)
- `Last_Contacted_Date` (Date property)
- `Rich_Text_Notes` (Text property)
- `I_Contacted_Them_Today` (Checkbox property)

### 2. Generate the Notion API Token
1. Go to [Notion Integrations](https://www.notion.so/my-integrations).
2. Click **New Integration**, name it "Personal CRM", and copy the **Internal Integration Token**.
3. Go back to your Notion Database. Click the `...` menu in the top right.
4. Scroll down and click **Connections**, then click **Connect to**, and search for "Personal CRM". Click it to grant the script access to your database.
5. Extract the **Database ID** from your Notion URL (it's the 32-character string between the workspace name and the `?v=` parameter).

### 3. Configure the Environment
1. In this directory, copy the template file to create your active env file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste your `NOTION_TOKEN` and `NOTION_DATABASE_ID`.
3. Set `USE_DISCORD` or `USE_EMAIL` to `true` and fill in the corresponding credentials:

**If using Discord:**
1. Open your Discord server and go to **Server Settings** > **Integrations** > **Webhooks**.
2. Click **New Webhook**, select the channel you want the CRM to post in, and click **Copy Webhook URL**.
3. Paste this into `DISCORD_WEBHOOK_URL` in your `.env` file.

**If using Gmail:**
1. You cannot use your normal Gmail password. Go to your [Google Account Security Settings](https://myaccount.google.com/security).
2. Ensure **2-Step Verification** is turned on.
3. Search for **App Passwords** in the search bar. 
4. Create a new App Password named "Personal CRM".
5. Copy the 16-character password and paste it into `SMTP_PASSWORD`. 
6. Set `SMTP_SERVER="smtp.gmail.com"` and `SMTP_PORT=587`.

### 4. Deploy the Engine (Homelab)
This script is designed to run 24/7 on your local homelab. It has an internal scheduler set to exactly 03:30 AM.
```bash
docker-compose up -d --build
```
You can now close the Proxmox web browser. The Docker container will run silently in the background of your homelab forever, waking up every morning at 3:30 AM to calculate your networking intervals.

## 5. Mobile UI Setup & Day-to-Day Use
The engine is automated, meaning your only interaction with this CRM is on your phone when you actually talk to someone.

**Setting up the Mobile View:**
1. Open the Notion app on your phone and go to your Personal CRM database.
2. Tap the `+` icon next to the current view name to create a new View.
3. Select **Gallery** or **List**.
4. Tap **Properties** and hide everything *except* the `Name` and the `I_Contacted_Them_Today` checkbox.
5. Tap **Sort**, select `Last_Contacted_Date`, and set it to **Ascending** (so the people you haven't spoken to the longest are at the top).

**The 5-Second Workflow:**
When you finish a coffee chat or text a contact:
1. Open the app and find their name.
2. **Check the `I_Contacted_Them_Today` box.**
3. (Optional) Type a quick note in `Rich_Text_Notes`.
*That's it. At 3:30 AM, the server will detect the checked box, update the date to today, uncheck the box for you, and move them to the bottom of your list!*
