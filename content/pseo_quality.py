"""
pSEO Quality Thresholds — single source of truth.
Used by: audit_pseo_quality command and seo_tags template tag.
"""

# Minimum word count for INDEX recommendation
PSEO_MIN_WORD_COUNT = 500

# Thresholds to trigger NOINDEX (both conditions must be true)
PSEO_NOINDEX_WORD_COUNT = 200   # below this → almost certainly thin
# Duplicate detection is done at audit time; per-page noindex is word-count driven.

# Categories
INDEX  = "INDEX"
REVIEW = "REVIEW"
NOINDEX = "NOINDEX"


def classify_page(word_count, has_structured_data, has_canonical, internal_link_count,
                  is_dup_title=False, is_dup_meta=False, is_dup_h1=False):
    """
    Return (recommendation, list_of_flags).
    Rules applied in priority order:
      1. NOINDEX  — word_count < PSEO_NOINDEX_WORD_COUNT
      2. REVIEW   — any quality flag present
      3. INDEX    — passes all checks
    """
    flags = []

    if word_count < PSEO_NOINDEX_WORD_COUNT:
        flags.append("thin_content")
        return NOINDEX, flags

    if word_count < PSEO_MIN_WORD_COUNT:
        flags.append("low_word_count")
    if not has_structured_data:
        flags.append("no_structured_data")
    if not has_canonical:
        flags.append("no_canonical")
    if internal_link_count < 3:
        flags.append("low_internal_links")
    if is_dup_title:
        flags.append("duplicate_title")
    if is_dup_meta:
        flags.append("duplicate_meta")
    if is_dup_h1:
        flags.append("duplicate_h1")

    if flags:
        return REVIEW, flags
    return INDEX, flags
