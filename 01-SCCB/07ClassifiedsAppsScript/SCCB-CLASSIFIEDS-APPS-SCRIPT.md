# SCCB-CLASSIFIEDS-APPS-SCRIPT: Google Apps Script for Free Classifieds Discovery

## Task Description
Build a Google Apps Script that discovers FREE classified ad portals for the specified countries using Google Search and records them into an existing Google Sheet.

**Google Sheet:**
https://docs.google.com/spreadsheets/d/1un4Gbix9M6nq9nY5N0LoKSEUxBF5BgoA9pdz6WqpYM0/edit

## Requirements
1. Open the above Google Spreadsheet.
2. Create a sheet named "Classifieds" if it does not already exist.
3. If it exists, append only new portals. Do not create duplicates based on domain.
4. Use Google Search (Custom Search API or Programmable Search Engine) via Google Apps Script to discover free classified websites. Use Google's supported search APIs rather than scraping Google search pages directly.

### Countries to process
USA, UK, Canada, Dubai, Bahrain, Abu Dhabi, Kuwait, Saudi Arabia, Singapore, Malaysia, South Africa, Botswana

### Search Queries
For each country search using multiple queries such as:
- free classifieds <country>
- free classified ads <country>
- post free ads <country>
- free business classifieds <country>
- free local classifieds <country>
- real estate classifieds <country>
- property classifieds <country>
- free advertising sites <country>

### Columns to capture
For every unique portal found, capture:
1. Country
2. Portal Name
3. Website
4. Home URL
5. Post Ad URL (if available)
6. Category (General / Real Estate / Business / Local)
7. Free Posting (Yes / No / Partial)
8. Registration Required (Yes / No)
9. Supports Real Estate (Yes / No)
10. Supports Business Services (Yes / No)
11. Domain
12. Status (Active / Inactive)
13. Last Verified Date
14. Notes

### Rules
- Only include active websites.
- Only include websites that allow free posting or have a free tier.
- Prefer well-known local portals over global directories.
- Remove duplicates by root domain.
- Ignore spam, parked domains, blogs, SEO directories, and article pages.
- Prefer the official website of the classified portal.
- Validate that the site is reachable before recording.

### Output
- Populate the "Classifieds" sheet with one row per portal.
- Add filters to the header row.
- Sort by Country and Portal Name.

### Custom Menu
Create a custom menu:
**Classifieds**
- Refresh All Countries
- Refresh Current Country
- Remove Duplicates
- Verify Links

### Modular functions required
- `searchCountry()`
- `extractPortal()`
- `verifyPortal()`
- `writeToSheet()`
- `removeDuplicates()`
- `refreshAll()`
- Custom Menu triggers

Include comments throughout the Apps Script. The script should be idempotent.
