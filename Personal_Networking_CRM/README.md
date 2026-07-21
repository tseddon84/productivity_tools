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
3. Set `USE_DISCORD` or `USE_EMAIL` to `true` and fill in the corresponding credentials.

### 4. Deploy the Engine (Homelab)
This script is designed to run 24/7 on your local homelab. It has an internal scheduler set to exactly 03:30 AM.
```bash
docker-compose up -d --build
```
The container will spin up, run the math once immediately, and then arm the 3:30 AM timer. You can walk away forever.
