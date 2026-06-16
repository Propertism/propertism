# Phase B Delta Report

Comparison of local SQLite (25 published articles) vs production PostgreSQL (13 published articles).

## Identification Methodology
By querying both local SQLite database (via `django.cmd` shell command) and production PostgreSQL (via EB SSH command execution), we verified:
- Local database contains 25 articles (all published).
- Production database contains 13 articles (all published).
- The intersection of the two lists contains exactly 13 articles.
- The delta represents exactly 12 missing articles on production.

## Missing Slugs (12 Articles)

These articles are present in local SQLite but missing from production PostgreSQL and must be synchronized:

| # | Article Title | Slug | Category |
|---|---|---|---|
| 1 | Complete Guide to Managing NRI Property in Chennai | `nri-property-management-guide-chennai` | `nri` |
| 2 | Top Challenges NRIs Face with Property Ownership in Chennai | `nri-property-ownership-challenges-chennai` | `nri` |
| 3 | NRI Property Checklist for Chennai Owners Living Abroad | `nri-property-checklist-chennai-owners-abroad` | `nri` |
| 4 | NRI Real Estate Investment in Chennai: A Complete Guide | `nri-real-estate-investment-chennai-guide` | `nri` |
| 5 | Step-by-Step NRI Property Buying Process in Chennai | `nri-property-buying-process-chennai` | `nri` |
| 6 | Common Mistakes NRI Property Buyers Make in Chennai | `common-mistakes-nri-property-buyers-chennai` | `nri` |
| 7 | What Property Services Do NRIs Need in Chennai? | `nri-property-services-chennai-guide` | `nri` |
| 8 | End-to-End NRI Property Services in Chennai Explained | `end-to-end-nri-property-services-chennai` | `nri` |
| 9 | How Propertism Simplifies Property Ownership for NRIs | `how-propertism-simplifies-nri-property-ownership` | `nri` |
| 10 | NRI Property Tax in Chennai: Complete Guide for 2026 | `nri-property-tax-chennai-guide` | `nri` |
| 11 | NRI Property Legal Compliance in Chennai: What You Must Know | `nri-property-legal-compliance-chennai` | `nri` |
| 12 | How to Choose an NRI Property Management Company in Chennai | `nri-property-management-company-chennai` | `nri` |
