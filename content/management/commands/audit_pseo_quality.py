"""
Management command: audit_pseo_quality

Audits all programmatically generated landing pages (Cities × Intents × NRI Locations)
and writes reports/pseo_quality_audit.csv.

Usage:
    python manage.py audit_pseo_quality
    python manage.py audit_pseo_quality --output path/to/custom.csv
    python manage.py audit_pseo_quality --city chennai
    python manage.py audit_pseo_quality --summary-only
"""
import csv
import os
import re
import sys
from collections import Counter

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import RequestFactory

from content.intent_mapping import CITIES, NRI_LOCATIONS, get_all_intents, get_intent_config
from content.pseo_quality import INDEX, NOINDEX, REVIEW, classify_page
from content.views_landing import landing_page


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_text(html, tag):
    """Extract the first occurrence of a tag's content from raw HTML."""
    pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return ""


def _meta_content(html, name):
    """Extract content attribute of a named meta tag."""
    pattern = rf'<meta[^>]+name=["\']?{re.escape(name)}["\']?[^>]+content=["\']([^"\']*)["\']'
    match = re.search(pattern, html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Try reversed attribute order
    pattern2 = rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']?{re.escape(name)}["\']?'
    match2 = re.search(pattern2, html, re.IGNORECASE)
    return match2.group(1).strip() if match2 else ""


def _canonical(html):
    """Extract canonical href."""
    match = re.search(r'<link[^>]+rel=["\']?canonical["\']?[^>]+href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match2 = re.search(r'<link[^>]+href=["\']([^"\']*)["\'][^>]+rel=["\']?canonical["\']?', html, re.IGNORECASE)
    return match2.group(1).strip() if match2 else ""


def _count_words(html):
    """Approximate visible word count by stripping tags."""
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(text.split())


def _has_structured_data(html):
    """True if any application/ld+json block is present."""
    return bool(re.search(r'application/ld\+json', html, re.IGNORECASE))


def _count_internal_links(html):
    """Count <a href="/..."> links (internal)."""
    return len(re.findall(r'<a\s[^>]*href=["\']/', html, re.IGNORECASE))


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = "Audit all pSEO landing pages and write reports/pseo_quality_audit.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=None,
            help="CSV output path (default: reports/pseo_quality_audit.csv)",
        )
        parser.add_argument(
            "--city",
            default=None,
            help="Limit audit to a single city slug",
        )
        parser.add_argument(
            "--summary-only",
            action="store_true",
            help="Print summary metrics only, do not write CSV",
        )

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        output_path = options["output"] or os.path.join(base_dir, "reports", "pseo_quality_audit.csv")
        city_filter = options["city"]
        summary_only = options["summary_only"]

        factory = RequestFactory()

        city_slugs = [city_filter] if city_filter and city_filter in CITIES else list(CITIES.keys())
        intent_slugs = get_all_intents()

        # Build full page inventory
        pages = []
        for city_slug in city_slugs:
            for intent_slug in intent_slugs:
                pages.append({"city": city_slug, "intent": intent_slug, "nri": None})
                for nri_slug in NRI_LOCATIONS.keys():
                    pages.append({"city": city_slug, "intent": intent_slug, "nri": nri_slug})

        total = len(pages)
        self.stdout.write(f"Auditing {total} pages across {len(city_slugs)} cities × {len(intent_slugs)} intents …")

        rows = []
        errors = 0

        for i, page in enumerate(pages, 1):
            city_slug = page["city"]
            intent_slug = page["intent"]
            nri_slug = page["nri"]

            if nri_slug:
                url = f"/{nri_slug}/{city_slug}-{intent_slug}/"
                try:
                    request = factory.get(url)
                    response = landing_page(request, city_slug, intent_slug, nri_origin=nri_slug)
                    html = response.content.decode("utf-8", errors="replace")
                except Exception as exc:
                    errors += 1
                    self.stderr.write(f"  ERROR {url}: {exc}")
                    continue
            else:
                url = f"/{city_slug}/{intent_slug}/"
                try:
                    request = factory.get(url)
                    response = landing_page(request, city_slug, intent_slug)
                    html = response.content.decode("utf-8", errors="replace")
                except Exception as exc:
                    errors += 1
                    self.stderr.write(f"  ERROR {url}: {exc}")
                    continue

            page_title = _extract_text(html, "title")
            meta_desc = _meta_content(html, "description")
            h1 = _extract_text(html, "h1")
            canonical = _canonical(html)
            word_count = _count_words(html)
            has_sd = _has_structured_data(html)
            internal_links = _count_internal_links(html)

            rows.append({
                "url": url,
                "page_title": page_title,
                "meta_description": meta_desc,
                "h1": h1,
                "canonical_url": canonical,
                "word_count": word_count,
                "structured_data": "yes" if has_sd else "no",
                "internal_links": internal_links,
                # duplicates filled in after full scan
                "_has_sd": has_sd,
                "_has_canonical": bool(canonical),
            })

            if i % 50 == 0:
                self.stdout.write(f"  … {i}/{total}")

        # --- Duplicate detection ---
        title_counts = Counter(r["page_title"] for r in rows if r["page_title"])
        meta_counts  = Counter(r["meta_description"] for r in rows if r["meta_description"])
        h1_counts    = Counter(r["h1"] for r in rows if r["h1"])

        dup_title_total = sum(1 for r in rows if title_counts[r["page_title"]] > 1)
        dup_meta_total  = sum(1 for r in rows if meta_counts[r["meta_description"]] > 1)
        dup_h1_total    = sum(1 for r in rows if h1_counts[r["h1"]] > 1)

        # --- Classification ---
        counts = {INDEX: 0, REVIEW: 0, NOINDEX: 0}
        for r in rows:
            rec, flags = classify_page(
                word_count=r["word_count"],
                has_structured_data=r["_has_sd"],
                has_canonical=r["_has_canonical"],
                internal_link_count=r["internal_links"],
                is_dup_title=(title_counts[r["page_title"]] > 1),
                is_dup_meta=(meta_counts[r["meta_description"]] > 1),
                is_dup_h1=(h1_counts[r["h1"]] > 1),
            )
            r["recommendation"] = rec
            r["flags"] = "|".join(flags)
            counts[rec] += 1

        # --- Summary ---
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("PSEO QUALITY AUDIT SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Total Pages Audited  : {len(rows)}")
        self.stdout.write(f"Render Errors Skipped: {errors}")
        self.stdout.write(f"INDEX Candidates     : {counts[INDEX]}")
        self.stdout.write(f"REVIEW Candidates    : {counts[REVIEW]}")
        self.stdout.write(f"NOINDEX Candidates   : {counts[NOINDEX]}")
        self.stdout.write(f"Duplicate Titles     : {dup_title_total}")
        self.stdout.write(f"Duplicate Meta Descs : {dup_meta_total}")
        self.stdout.write(f"Duplicate H1s        : {dup_h1_total}")
        self.stdout.write("=" * 60)

        if summary_only:
            return

        # --- Write CSV ---
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fieldnames = [
            "url", "page_title", "meta_description", "h1",
            "canonical_url", "word_count", "structured_data",
            "internal_links", "recommendation", "flags",
        ]
        with open(output_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

        self.stdout.write(self.style.SUCCESS(f"\nCSV written → {output_path}"))
