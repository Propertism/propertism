"""
Management command: spam_inquiries

Handles two distinct spam categories:
1. 40,000+ historical Russian/Cyrillic ad spam: HARD PURGED (never moves to SpamLog).
2. Recent English bot suspects (RobertTharp, DylanUncer, etc.): Quarantined to SpamLog.

Usage:
  # Count only -- safe read-only breakdown:
  python manage.py spam_inquiries --count

  # Clean all -- hard purges 40k+ Cyrillic, quarantines only recent bots to SpamLog:
  python manage.py spam_inquiries --clean-all --confirm

  # Purge 40k+ Cyrillic only (direct deletion, zero SpamLog bloat):
  python manage.py spam_inquiries --purge-cyrillic --confirm

  # Quarantine recent English bot suspects only to SpamLog:
  python manage.py spam_inquiries --quarantine-bots --confirm
"""

import re

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from properties.models import Inquiry

_CYRILLIC_RE = re.compile(r"[\u0400-\u052F]")
_BOT_NAME_RE = re.compile(r"^[A-Z][a-z]{2,}[A-Z][a-zA-Z]{2,}$")


def _is_cyrillic(name, message):
    return bool(_CYRILLIC_RE.search(name or "") or _CYRILLIC_RE.search(message or ""))


def _is_bot_lead(name, message, assessment_status):
    if _BOT_NAME_RE.match((name or "").strip()):
        return True, "Concatenated Bot Name"
    if assessment_status == "Likely Spam":
        return True, "Likely Spam Assessment"
    if "wellorena.com" in (message or "").lower() or "share.google" in (message or "").lower():
        return True, "Affiliate Link Injection"
    return False, ""


class Command(BaseCommand):
    help = (
        "Purge 40k+ Cyrillic spam directly and quarantine only recent bot suspects to SpamLog."
    )

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--count",
            action="store_true",
            help="Report count breakdown of Cyrillic spam vs recent bot suspects (read-only).",
        )
        group.add_argument(
            "--clean-all",
            action="store_true",
            help="Purge Cyrillic spam directly and quarantine only recent bot suspects to SpamLog. REQUIRES --confirm.",
        )
        group.add_argument(
            "--purge-cyrillic",
            action="store_true",
            help="Directly delete 40k+ Cyrillic spam (zero SpamLog bloat). REQUIRES --confirm.",
        )
        group.add_argument(
            "--quarantine-bots",
            action="store_true",
            help="Move only recent English bot suspects into SpamLog. REQUIRES --confirm.",
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            default=False,
            help="Required alongside execution flags.",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            "\n[spam_inquiries] Run at %s\n" % timezone.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        )

        all_rows = list(Inquiry.objects.values_list("id", "name", "message", "assessment_status"))
        total = len(all_rows)

        cyrillic_ids = []
        bot_records = []

        for row in all_rows:
            inq_id, name, message, status = row[0], row[1], row[2], row[3]
            if _is_cyrillic(name, message):
                cyrillic_ids.append(inq_id)
            else:
                is_bot, reason = _is_bot_lead(name, message, status)
                if is_bot:
                    bot_records.append((inq_id, reason))

        cyrillic_count = len(cyrillic_ids)
        bot_count = len(bot_records)
        legitimate_count = total - (cyrillic_count + bot_count)

        self.stdout.write("  Total inquiries in DB           : %d" % total)
        self.stdout.write("  Historical Cyrillic spam (40k+) : %d  (Target: Direct Purge)" % cyrillic_count)
        self.stdout.write("  Recent English bot suspects     : %d  (Target: Quarantine to SpamLog)" % bot_count)
        self.stdout.write("  Legitimate genuine leads        : %d\n" % legitimate_count)

        if options["count"]:
            self.stdout.write(
                "  [READ-ONLY] No data modified. Run with --clean-all --confirm to clean up.\n"
            )
            return

        if not options["confirm"]:
            self.stderr.write("  ERROR: Execution requires --confirm flag.\n")
            return

        # Execute Clean-All or specific operations
        if options["clean_all"] or options["purge_cyrillic"]:
            if cyrillic_ids:
                self.stdout.write("  Purging %d Cyrillic spam records directly from Inquiry table..." % cyrillic_count)
                with transaction.atomic():
                    deleted_cyr, _ = Inquiry.objects.filter(id__in=cyrillic_ids).delete()
                self.stdout.write("  PURGED %d Cyrillic records (zero SpamLog bloat)." % deleted_cyr)
            else:
                self.stdout.write("  No Cyrillic spam records found to purge.")

        if options["clean_all"] or options["quarantine_bots"]:
            if bot_records:
                from content.models import SpamLog
                bot_ids = [r[0] for r in bot_records]
                self.stdout.write("  Quarantining %d recent bot suspects to SpamLog..." % bot_count)
                bot_qs = Inquiry.objects.filter(id__in=bot_ids)
                with transaction.atomic():
                    moved = 0
                    for item in bot_qs:
                        SpamLog.objects.create(
                            ip_address="127.0.0.1",
                            user_agent="Management Command Quarantine",
                            form_name=item.form_source or "Inquiry Table",
                            request_path="/admin/properties/inquiry/",
                            failure_reason=f"CLI Quarantined ({item.assessment_status or 'Bot Pattern'})",
                            confidence_score=item.confidence_score or 0,
                            name=item.name,
                            email=item.email,
                            phone=item.phone,
                            message=item.message,
                            country_code=item.country_code or "",
                            country_name=item.country_name or "",
                            validation_summary=item.validation_summary or [],
                        )
                        moved += 1
                    deleted_bots, _ = bot_qs.delete()
                self.stdout.write("  QUARANTINED %d recent bot suspects to SpamLog table." % moved)
            else:
                self.stdout.write("  No recent bot suspects found to quarantine.")

        remaining = Inquiry.objects.count()
        self.stdout.write("\n  DONE. Clean Inquiry table now contains %d legitimate leads.\n" % remaining)
