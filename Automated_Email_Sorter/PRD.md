# Product Requirements Document (PRD)

## 1. Executive Summary & Product Overview
**Product Name:** Automated Email Sorter & Summarizer
**Problem Statement:** Inboxes are flooded with newsletters, cold outreach, and non-urgent notifications. Native Gmail filters are rigid and require constant maintenance. Reading all non-urgent mail consumes significant cognitive bandwidth.
**Target Audience:** Professionals seeking a "Zero-Inbox" state without manually archiving or reading bulk mail.
**Core Value Proposition:** A completely serverless AI assistant built in Google Apps Script that acts as a bouncer for the inbox. It catches unread mail, categorizes it using the Gemini API, applies Gmail labels, and compiles low-priority text into a single Daily Digest.
**Success Metrics:** The script accurately categorizes emails and successfully compiles a digest without interfering with the user's native Gmail Boolean filters.
**Out of Scope:** Sending automated AI-generated replies to human senders.

## 2. Tech Stack & Architecture
**Execution Environment:** Google Apps Script (runs 100% serverless on Google's cloud).
**Trigger Mechanism:** Time-driven trigger (cron) running every 15 minutes, or a Pub/Sub trigger tied to Gmail inbox updates.
**APIs & Integrations:**
- **Gmail Service (Native App Script Object):** Used to query the inbox, apply labels, and archive emails.
- **Google Gemini API:** Used to parse the email body, return a strict category, and generate a 2-sentence summary.
**Security:** All API calls are executed strictly server-side. The configuration block clearly warns users about Free vs Paid API privacy SLAs.

## 3. Core Features & Requirements
- **Feature 1: The Free/Paid Privacy Router**
  - A strict configuration toggle (`USE_FREE_TIER_PRIVACY_FILTER`).
  - If `TRUE`, the script executes a pre-flight RegEx check against a hardcoded list of sensitive domains (`@chase.com`, `@my-doctor.com`). Sensitive emails are immediately skipped and left for the user, preventing private data from hitting the free LLM tier.
  - If `FALSE`, the script sends all targets to the Gemini API under the Paid Tier privacy guarantee.
- **Feature 2: Symbiotic Inbox Querying**
  - The script's querying logic is hardcoded to target only `is:unread in:inbox`.
  - This ensures the AI completely ignores any emails that were already moved or archived by the user's native Gmail Filters, preventing race conditions and saving API tokens.
- **Feature 3: The Categorization & Labeling Engine**
  - The LLM processes the email body and returns a rigid JSON schema specifying the category (e.g., `Urgent`, `Newsletter`, `Receipt`).
  - The Apps Script receives the JSON, dynamically creates the Gmail Label if it doesn't exist, applies it, and removes the `Inbox` label (archiving it).
- **Feature 4: The Daily Digest Compiler**
  - For emails categorized as `Newsletter` or `Updates`, the LLM's 2-sentence summary is appended to a hidden **Google Sheet**, which acts as a robust database.
  - A secondary trigger runs at 5:00 PM, pulling all un-sent rows from the Sheet, compiling them into a beautifully formatted HTML email digest, and marking those rows as "Sent".
- **Feature 5: Programmatic Trigger Configuration**
  - Instead of requiring manual UI trigger setup, the configuration block includes a `RUN_FREQUENCY_MINUTES` variable.
  - An `install()` function utilizes the native `ScriptApp` class to dynamically clear old triggers and generate a new time-driven trigger based strictly on the user's declared frequency (e.g., 5, 15, or 60 minutes), allowing users to seamlessly manage their Google Quota limits.
- **Feature 6: Comprehensive Setup Documentation**
  - A heavily detailed `README.md` must be included in the project directory.
  - It must explicitly outline the privacy risks of the Free Tier vs. Paid Tier API keys.
  - It must provide step-by-step instructions on acquiring the API key, configuring the script variables, and executing the `install()` function.
