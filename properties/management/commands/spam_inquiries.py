"""
Management command: spam_inquiries

Counts (and optionally deletes) Cyrillic-text spam inquiries from the
properties_inquiry table.

Usage:
  # Count only -- safe read-only report:
  python manage.py spam_inquiries --count

  # Delete (requires explicit --confirm flag):
  python manage.py spam_inquiries --delete --confirm

Detection logic:
  Any inquiry whose name OR message contains at least one Cyrillic Unicode
  character (U+0400-U+04FF, U+0500-U+052F) is considered spam.
"""

import re

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from properties.models import Inquiry

_CYRILLIC_RE = re.compile(r"[\u0400-\u052F]")


def _is_cyrillic(text):
    return bool(_CYRILLIC_RE.search(text or ""))


class Command(BaseCommand):
    help = (
        "Count (and optionally delete) Cyrillic/Russian spam inquiries. "
        "Run with --count for a safe read-only report."
    )

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--count",
            action="store_true",
            help="Report the total count of Cyrillic spam inquiries (read-only).",
        )
        group.add_argument(
            "--delete",
            action="store_true",
            help="Delete all Cyrillic spam inquiries. REQUIRES --confirm.",
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            default=False,
            help="Required alongside --delete to actually execute deletion.",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            "\n[spam_inquiries] Run at %s\n" % timezone.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        )

        self.stdout.write("  Scanning inquiries for Cyrillic content...")
        all_rows = list(Inquiry.objects.values_list("id", "name", "message"))
        spam_ids = [
            row[0]
            for row in all_rows
            if _is_cyrillic(row[1]) or _is_cyrillic(row[2])
        ]
        total = len(all_rows)
        spam_count = len(spam_ids)

        self.stdout.write("\n  Total inquiries in DB : %d" % total)
        self.stdout.write("  Cyrillic spam records : %d" % spam_count)
        self.stdout.write("  Legitimate records    : %d\n" % (total - spam_count))

        if options["count"]:
            from django.db.models import Count as DjCount
            breakdown = (
                Inquiry.objects.filter(id__in=spam_ids)
                .values("assessment_status")
                .annotate(n=DjCount("id"))
                .order_by("-n")
            )
            if breakdown:
                self.stdout.write("  Breakdown by assessment_status:")
                for row in breakdown:
                    self.stdout.write(
                        "    %-30s  %6d" % (row["assessment_status"] or "None", row["n"])
                    )

            fs_breakdown = (
                Inquiry.objects.filter(id__in=spam_ids)
                .values("form_source")
                .annotate(n=DjCount("id"))
                .order_by("-n")[:10]
            )
            if fs_breakdown:
                self.stdout.write("\n  Top form sources (spam):")
                for row in fs_breakdown:
                    self.stdout.write(
                        "    %-40s  %6d" % (row["form_source"] or "None", row["n"])
                    )

            self.stdout.write(
                "\n  [READ-ONLY] No data was modified. Run with --delete --confirm to delete.\n"
            )
            return

        if options["delete"] and not options["confirm"]:
            self.stderr.write(
                "  ERROR: --delete requires --confirm. Add --confirm to execute the deletion.\n"
            )
            return

        if not spam_ids:
            self.stdout.write("  No Cyrillic spam records found. Nothing to delete.\n")
            return

        self.stdout.write("  Deleting %d Cyrillic spam inquiries..." % spam_count)
        with transaction.atomic():
            deleted_count, _ = Inquiry.objects.filter(id__in=spam_ids).delete()

        self.stdout.write(
            "  DONE -- deleted %d records. Remaining: %d.\n"
            % (deleted_count, total - deleted_count)
        )
