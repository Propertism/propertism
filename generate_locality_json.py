#!/usr/bin/env python
"""
generate_locality_json.py — Generate locality_registry.json for Deal Engine sync.

Run this script any time content/locality_registry.py is updated.
Commits the resulting JSON to both propertism.in and deal engine repos.

Usage:
    python generate_locality_json.py
"""

import json
import os
import sys

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content.locality_registry import LOCALITY_REGISTRY, get_dropdown_choices, get_extraction_keywords

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locality_registry.json")

# Also export to the deal engine repo if it exists
DEAL_ENGINE_ALT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "06propertism.deal.engine", "locality_registry.json"
)

def main():
    payload = {
        "_meta": {
            "version": "1.0",
            "source": "content/locality_registry.py",
            "description": "Canonical locality registry. Edit locality_registry.py, not this JSON.",
            "dropdown_count": len(get_dropdown_choices()),
            "extraction_keyword_count": len(get_extraction_keywords()),
        },
        "registry": LOCALITY_REGISTRY,
        "dropdown_choices": [{"slug": s, "display": d} for s, d in get_dropdown_choices()],
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Written: {OUTPUT_PATH} ({len(LOCALITY_REGISTRY)} entries)")

    # Write to Deal Engine if path exists
    if os.path.exists(os.path.dirname(DEAL_ENGINE_ALT)):
        with open(DEAL_ENGINE_ALT, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"Written: {DEAL_ENGINE_ALT}")
    else:
        print(f"Deal Engine path not found, skipping: {DEAL_ENGINE_ALT}")


if __name__ == "__main__":
    main()