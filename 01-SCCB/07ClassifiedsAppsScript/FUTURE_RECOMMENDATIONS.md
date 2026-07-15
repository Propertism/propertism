# Future Recommendations: Classifieds Portal Aggregator

Based on the implementation of the Google Apps Script aggregator, we recommend the following enhancements to maximize automation and data quality:

## 1. Trigger Automation
- **Scheduled Triggers**: Set up a time-driven trigger in Google Apps Script (e.g. monthly or bi-weekly) to automatically run `verifyAllLinks()` to verify if portals are still active and clean up dead URLs without manual action.

## 2. API Quota Optimization
- **Custom Search API Limits**: The free tier of the Google Custom Search API is capped at 100 queries/day. If all 12 countries are refreshed using the full list of 8 queries, it requires 96 API queries.
- **Recommendations**:
  - Keep the default search query count optimized (3 high-impact queries per country as configured).
  - Use `Refresh Current Country` when building out specific target locations to avoid running out of daily quota.
  - For full coverage, upgrade to a billing-enabled Google Cloud Search Console API key ($5 per 1,000 queries beyond the 100 free daily).

## 3. Advanced Crawler Integration
- **Proxies/Fetch Hardening**: Some high-traffic classified sites use Cloudflare or rate-limit standard Google Apps Script IP ranges, returning 403/503 status codes. 
- **Recommendation**: If link validation reports active sites as `Inactive` due to Cloudflare protection, configure the validator to flag status as `Verification Blocked` rather than `Inactive`, keeping them visible in the sheet for manual confirmation.
