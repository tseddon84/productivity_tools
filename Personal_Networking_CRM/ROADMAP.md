# Roadmap: Personal Networking CRM

## Current Version: v0.1.0
- Automated daily processing via Docker scheduling (03:30 AM).
- Notion API integration for fetching and parsing contact intervals.
- Interval calculation based on connection strength.
- Discord and Email notifications for overdue contacts.
- Frictionless mobile-optimized Notion UI workflow.

## Future Enhancements

### 1. Database Schema Expansion
Expand the Notion database schema to transition away from relying solely on a single `Rich_Text_Notes` field. Adding dedicated, structured fields will allow for better filtering, sorting, and more granular memory tracking.

**Planned Fields to Add:**
- [ ] Birthday
- [ ] Spouse
- [ ] Spouse's Birthday
- [ ] Kids
- [ ] Kids' Birthdays
- [ ] Pets
- [ ] Likes
- [ ] Dislikes
- [ ] Shared Activities
- [ ] Preferred Method of Contact
- [ ] Contact Information

### 2. Notification Engine Updates
- Once the new database fields are added, update the Python script to parse these new fields and intelligently inject them into the automated morning outreach summaries.
