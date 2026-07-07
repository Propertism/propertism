# Future Recommendations: Website Conversational Knowledge Extraction

**SCCB Document Reference**: [SCCB-PROP-RBOT-KNOWLEDGE-WEBSITE-QA-EXTRACTION-001](file:///d:/viji/viji-olivine/03rolledout/01propertism/01-SCCB/06WebsiteQAExtraction/SCCB-PROP-RBOT-KNOWLEDGE-WEBSITE-QA-EXTRACTION-001.md)
**Author**: Antigravity AI
**Date**: 2026-07-07

---

## Strategic Recommendations

1. **Scheduled Extraction Cron Job**:
   - Currently, extraction is triggered via an administrative REST API endpoint. We recommend scheduling a lightweight cron job (e.g., nightly) to automatically run extraction and flag new candidates or updates for administrator review.
   
2. **Enhanced Synonym Expansion Mapping**:
   - Investigate adding a localized dictionary of common Tamil and South Indian name splits or variations (e.g. "Viji" -> "Vijay", "Tamilselvan" -> "Tamilselvan Munuswamy") to make the deterministic synonym generator even more comprehensive.

3. **Incremental DB Cleanups**:
   - Ensure the `ExtractedKnowledgeCandidate` table is periodically pruned of rejected or published candidates that are older than 90 days to prevent excessive database size expansion.
