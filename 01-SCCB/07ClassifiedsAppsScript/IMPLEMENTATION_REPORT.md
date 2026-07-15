# SCCB Implementation Report: Classifieds Portal Apps Script

## Implementation Overview
We designed and implemented a production-grade, modular, and idempotent Google Apps Script to discover, validate, and catalog free classified ad portals for 12 target countries (USA, UK, Canada, Dubai, Bahrain, Abu Dhabi, Kuwait, Saudi Arabia, Singapore, Malaysia, South Africa, and Botswana).

The solution has been saved in the repository at:
[ClassifiedsAggregator.js](file:///d:/viji/viji-olivine/03rolledout/01propertism/01-SCCB/07ClassifiedsAppsScript/ClassifiedsAggregator.js)

---

## Architectural Details & Modular Functions

### 1. Discovery Pipeline (`searchCountry`)
- Iterates through the list of targeted search queries per country.
- Calls Google's **Custom Search JSON API** (`https://www.googleapis.com/customsearch/v1`) using `UrlFetchApp.fetch`.
- Employs domain extraction to identify unique portals and ignores major search engines, blogging platforms, and social networks (e.g. facebook.com, blogspot.com, pinterest.com) using a hardcoded exclusion list.

### 2. Information Extraction (`extractPortal`)
- Strips trailing page/title suffixes (e.g. ` - Home`, ` | General Classifieds`).
- Classifies the portal into a target **Category** (`General`, `Real Estate`, `Business`, `Local`) by scanning the result title and snippet for relevant keywords.
- Predicts supports flags (`Supports Real Estate`, `Supports Business Services`) based on keyword indicators.

### 3. Validation & Scraping Engine (`verifyPortal`)
- Performed via a non-blocking `UrlFetchApp.fetch()` with a browser-realistic `User-Agent`.
- Validates that the domain returns a success code (`HTTP 200/301/302`) and marks unreachable links as `Inactive`.
- Parses the target site's homepage HTML (lightweight DOM scanning) to extract:
  - The precise **Post Ad URL** (by looking for anchors matching "post ad", "add listing", etc.).
  - **Registration Required** status (checking for login/signup triggers).
  - Category capability verification.

### 4. Idempotent Storage & UI Formatting (`writeToSheet`)
- Dynamically creates the **Classifieds** sheet in the Google Spreadsheet if it does not already exist.
- Implements a root-domain mapping lookup before writing:
  - **New domains**: Appended at the end of the sheet.
  - **Existing domains**: Row details are updated in place, retaining manual edits or comments while updating status and timestamps.
- Applies standard Propertism Navy (`#0F172A`) and Gold (`#B89A4A`) branding to the frozen header, sets date cell formatting, and enables filters.
- Sorts data by **Country** and then **Portal Name**.

### 5. Utilities & UI Menus
- **`removeDuplicates`**: Dedupes any duplicate domain entries in post-processing.
- **`verifyAllLinks`**: Batch pings all stored portals to update status and last verified date.
- **`refreshCurrentCountry`**: Prompts the user via `Browser.inputBox` to input a specific country, preserving Google Search API quota.

---

## Deployment Steps
1. Open the Google Spreadsheet: https://docs.google.com/spreadsheets/d/1un4Gbix9M6nq9nY5N0LoKSEUxBF5BgoA9pdz6WqpYM0/edit
2. Click **Extensions > Apps Script**.
3. Clear default code, copy the contents of [ClassifiedsAggregator.js](file:///d:/viji/viji-olivine/03rolledout/01propertism/01-SCCB/07ClassifiedsAppsScript/ClassifiedsAggregator.js) and paste it.
4. Click the Save icon.
5. Set up API credentials:
   - Go to **Project Settings** (gear icon).
   - Under **Script Properties**, add two entries:
     - `API_KEY` = `<Your Google Custom Search JSON API Key>`
     - `SEARCH_ENGINE_ID` = `<Your Search Engine ID>`
6. Refresh the spreadsheet. The **Classifieds** menu will appear.
