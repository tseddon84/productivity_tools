# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Versioning Rules for this Project:**
- **MAJOR (X.y.z):** Breaking changes. (e.g., A change requiring the user to update their Google Sheet schema/columns).
- **MINOR (x.Y.z):** Backward-compatible feature additions.
- **PATCH (x.y.Z):** Bug fixes or silent error resolutions.

---

## [1.0.0] - 2026-07-20
### Added
- **Circuit Breaker Limits:** Implemented a strict 3-task limit per category. Prevents task bankruptcy.
- **Specific Day Scheduling:** The `Frequency` column now accepts exact days (e.g., "Monday", "Friday") instead of just "Weekly".
- **Weekly Progress Metrics:** Upgraded the Sunday Review automation to query the Tasks API and output a 7-day historical completion tally.
- **Respawn Suppression:** Script now checks recently completed tasks (last 7 days) and suppresses duplicates for one-off Project Backlog tasks.

## [0.3.1] - 2026-07-20
### Fixed
- **Duplication Bug:** Fixed a critical bug where the daily trigger would blindly replicate existing tasks if run multiple times. Introduced `ensureTaskExists()` to query active tasks before insertion.

## [0.3.0] - 2026-07-19
### Added
- **Weekly Task Support:** Added logic to detect "Weekly" habits and drop them on Monday mornings.

## [0.2.1] - 2026-07-19
### Fixed
- **Schema Strictness (Silent Failures):** Addressed the `TypeError: Cannot read properties of null` bug caused by trailing spaces in spreadsheet tab names. Strict naming conventions enforced.

## [0.2.0] - 2026-07-18
### Added
- **Initial Code Draft:** Wrote the first working version of `ProductivityAutomations.gs`.
- **Schema Definition:** Built the initial 3-tab strict Google Sheet database schema (`Recurring Habits`, `Project Backlog`, `Household Cleaning Queue`).

## [0.1.0] - 2026-07-18
### Changed
- **[MIGRATION REQUIRED] Architecture Pivot:** Pivoted architecture away from Google Keep (due to Apps Script limitations) and standardized entirely on Google Tasks for the execution hub.
### Added
- **Sunday Review:** Conceived the "Sunday Review" calendar injection to solve the "Two-Way Sync Trap" without risking database corruption.
