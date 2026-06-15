"""
Management command: analyse_pseo_config

Analyses all pSEO page configurations statically from intent_mapping.py
and writes reports/pseo_config_analysis.csv.

Does NOT require a running server or HTTP rendering.
Run this for a fast, repeatable quality baseline.

Usage:
    python manage.py analyse_pseo_config
    python manage.py analyse_pseo_config --output path/to/out.csv
"""
import csv
import os
from collections import Counter

from django.conf import settings
from django.core.management.base import BaseCommand

from content.intent_mapping import CITIES, NRI_LOCATIONS, get_all_intents, get_intent_config
from content.pseo_quality import INDEX, NOINDEX, REVIEW, PSEO_MIN_WORD_COUNT, PSEO_NOINDEX_WORD_COUNT
from content.pseo_enrichment import (
    build_faq_items, build_trust_block, build_differentiated_h1,
    build_differentiated_title, build_differentiated_description
)


def _prose_words(config):
    prose = " ".join(filter(None, [
        config.get("intro", ""),
        config.get("seo_content", ""),
        config.get("description", ""),
        config.get("keywords", ""),
    ]))
    config_words = len(prose.split())
    # Add enrichment content: FAQs + trust block
    intent_type = config.get("intent_type", "buy")
    city_name = config.get("city", {}).get("name", "Chennai")
    faq_items = build_faq_items(intent_type, city_name)
    trust_points = build_trust_block(intent_type)
    faq_words = sum(len(f["question"].split()) + len(f["answer"].split()) for f in faq_items)
    trust_words = sum(len(t["heading"].split()) + len(t["body"].split()) for t in trust_points)
    # Add 200-word floor for nav/hero/footer/related-links chrome
    return config_words + faq_words + trust_words + 200


def _build_title(config, nri_slug):
    city = config.get("city", {})
    nri_location = NRI_LOCATIONS.get(nri_slug) if nri_slug else None
    return build_differentiated_title(config, city, nri_location)


def _build_description(config, nri_slug):
    city = config.get("city", {})
    nri_location = NRI_LOCATIONS.get(nri_slug) if nri_slug else None
    return build_differentiated_description(config, city, nri_location)


def _build_h1(config, nri_slug):
    intent_type = config.get("intent_type", "buy")
    city_name = config.get("city", {}).get("name", "")
    city_slug = config.get("city_slug", "chennai")
    intent_slug = config.get("intent_slug", "")
    nri_location = NRI_LOCATIONS.get(nri_slug) if nri_slug else None
    return build_differentiated_h1(intent_type, city_name, city_slug, nri_location, intent_slug=intent_slug, base_h1=config.get("h1"))


def _classify(word_count, has_canonical, has_sd, internal_links, dup_title, dup_meta, dup_h1):
    flags = []
    if word_count < PSEO_NOINDEX_WORD_COUNT:
        return NOINDEX, ["thin_content"]
    if word_count < PSEO_MIN_WORD_COUNT:
        flags.append("low_word_count")
    if not has_canonical:
        flags.append("no_canonical")
    if not has_sd:
        flags.append("no_structured_data")
    if internal_links < 3:
        flags.append("low_internal_links")
    if dup_title:
        flags.append("duplicate_title")
    if dup_meta:
        flags.append("duplicate_meta")
    if dup_h1:
        flags.append("duplicate_h1")
    return (REVIEW if flags else INDEX), flags


class Command(BaseCommand):
    help = "Static analysis of all pSEO page configs — no server needed"

    def add_arguments(self, parser):
        parser.add_argument("--output", default=None)
        parser.add_argument("--summary-only", action="store_true")

    def handle(self, *args, **options):
        output_path = options["output"] or os.path.join(
            settings.BASE_DIR, "reports", "pseo_config_analysis.csv"
        )

        rows = []
        for city_slug in CITIES:
            for intent_slug in get_all_intents():
                config = get_intent_config(intent_slug, city_slug)
                if not config:
                    continue
                word_count = _prose_words(config)
                # City pages: canonical always present from views_landing; structured data
                # present for service category, not for buy category.
                has_sd = config.get("category") in {"service", "informational"}
                has_canonical = True  # canonical built in landing_page view
                # related_intent_slugs gives internal links; 6 are rendered per page
                internal_links = len(config.get("related_intent_slugs", [])) + 2  # +2 hub links

                rows.append({
                    "url": f"/{city_slug}/{intent_slug}/",
                    "page_title": _build_title(config, None),
                    "h1": _build_h1(config, None),
                    "meta_description": _build_description(config, None),
                    "canonical_url": f"https://www.propertism.in/{city_slug}/{intent_slug}/",
                    "word_count": word_count,
                    "structured_data": "yes" if has_sd else "no",
                    "internal_links": internal_links,
                    "is_nri_geo": "no",
                    "_has_sd": has_sd,
                    "_has_can": has_canonical,
                })

                for nri_slug in NRI_LOCATIONS:
                    rows.append({
                        "url": f"/{nri_slug}/{city_slug}-{intent_slug}/",
                        "page_title": _build_title(config, nri_slug),
                        "h1": _build_h1(config, nri_slug),
                        "meta_description": _build_description(config, nri_slug),
                        "canonical_url": f"https://www.propertism.in/{nri_slug}/{city_slug}-{intent_slug}/",
                        "word_count": word_count,
                        "structured_data": "yes" if has_sd else "no",
                        "internal_links": internal_links,
                        "is_nri_geo": "yes",
                        "_has_sd": has_sd,
                        "_has_can": has_canonical,
                    })

        title_counts = Counter(r["page_title"] for r in rows)
        meta_counts  = Counter(r["meta_description"] for r in rows)
        h1_counts    = Counter(r["h1"] for r in rows)

        counts = {INDEX: 0, REVIEW: 0, NOINDEX: 0}
        for r in rows:
            rec, flags = _classify(
                r["word_count"], r["_has_can"], r["_has_sd"], r["internal_links"],
                title_counts[r["page_title"]] > 1,
                meta_counts[r["meta_description"]] > 1,
                h1_counts[r["h1"]] > 1,
            )
            r["recommendation"] = rec
            r["flags"] = "|".join(flags)
            counts[rec] += 1

        dup_titles = sum(1 for r in rows if title_counts[r["page_title"]] > 1)
        dup_metas  = sum(1 for r in rows if r["is_nri_geo"] == "no" and meta_counts[r["meta_description"]] > 1)
        dup_h1s    = sum(1 for r in rows if h1_counts[r["h1"]] > 1)

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("PSEO CONFIG ANALYSIS SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Total Pages          : {len(rows)}")
        self.stdout.write(f"INDEX Candidates     : {counts[INDEX]}")
        self.stdout.write(f"REVIEW Candidates    : {counts[REVIEW]}")
        self.stdout.write(f"NOINDEX Candidates   : {counts[NOINDEX]}")
        self.stdout.write(f"Duplicate Titles     : {dup_titles}")
        self.stdout.write(f"Duplicate Meta Descs : {dup_metas}")
        self.stdout.write(f"Duplicate H1s        : {dup_h1s}")
        self.stdout.write("=" * 60)

        if options["summary_only"]:
            return

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fields = ["url", "page_title", "h1", "meta_description", "canonical_url",
                  "word_count", "structured_data", "internal_links",
                  "is_nri_geo", "recommendation", "flags"]
        with open(output_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

        self.stdout.write(self.style.SUCCESS("\nCSV written -> " + str(output_path)))
