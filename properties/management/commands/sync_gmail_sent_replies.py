"""
sync_gmail_sent_replies — Backfill InquiryReply from Gmail Sent Mail.

Usage:
    python manage.py sync_gmail_sent_replies
    python manage.py sync_gmail_sent_replies --dry-run
    python manage.py sync_gmail_sent_replies --limit 1000 --since 2026-01-01

Required env var:
    GMAIL_APP_PASS  (16-char Gmail App Password)
    Windows: $env:GMAIL_APP_PASS = "xxxx-xxxx-xxxx-xxxx"
    Generate: myaccount.google.com/apppasswords
"""

import email
import imaplib
import os
from datetime import datetime, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from properties.models import Inquiry, InquiryReply

GMAIL_USER = os.environ.get("GMAIL_USER", "propertism.tamil@gmail.com")
IMAP_HOST = "imap.gmail.com"
SENT_LABEL = "[Gmail]/Sent Mail"


def _decode_hdr(value):
    if not value:
        return ""
    parts = decode_header(value)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return " ".join(result)


def _bare_addr(raw):
    raw = (raw or "").strip()
    if "<" in raw:
        return raw.split("<")[-1].rstrip(">").strip().lower()
    return raw.lower()


def _plain_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in disp:
                cs = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(cs, errors="replace")
    else:
        cs = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(cs, errors="replace")
    return ""


def _parse_date(raw):
    try:
        return parsedate_to_datetime(raw)
    except Exception:
        return None


class Command(BaseCommand):
    help = "Backfill InquiryReply from Gmail Sent Mail (propertism.tamil@gmail.com)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", type=int, default=500,
            help="Max sent emails to scan (default: 500)",
        )
        parser.add_argument(
            "--dry-run", action="store_true", default=False,
            help="Preview without writing to DB",
        )
        parser.add_argument(
            "--since", type=str, default=None,
            help="Only import emails on/after YYYY-MM-DD",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        dry_run = options["dry_run"]
        since_str = options["since"]

        since_date = None
        if since_str:
            try:
                since_date = datetime.strptime(since_str, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                raise CommandError(
                    "Invalid --since date. Use YYYY-MM-DD format."
                )

        # Accept GMAIL_APP_PASS or fall back to EMAIL_HOST_PASSWORD (same App Password)
        app_pass = (
            os.environ.get("GMAIL_APP_PASS")
            or os.environ.get("EMAIL_HOST_PASSWORD", "")
        )
        if not app_pass:
            raise CommandError(
                "No Gmail App Password found.\n"
                "Set GMAIL_APP_PASS or EMAIL_HOST_PASSWORD env var.\n"
                "Generate at: myaccount.google.com/apppasswords"
            )

        # 1. Load inquiries from DB
        self.stdout.write("Loading inquiries from DB...")
        all_inqs = list(Inquiry.objects.values("id", "email", "name", "status"))
        inq_map = {}
        for inq in all_inqs:
            key = inq["email"].strip().lower()
            inq_map.setdefault(key, []).append(inq)
        self.stdout.write(
            "  {} inquiries | {} unique emails".format(len(all_inqs), len(inq_map))
        )

        # 2. Load existing replies for dedup
        self.stdout.write("Loading existing InquiryReply records...")
        existing = set(
            InquiryReply.objects.values_list("to_email", "subject")
        )
        self.stdout.write("  {} existing replies".format(len(existing)))

        # 3. Connect to Gmail IMAP
        self.stdout.write("Connecting to Gmail IMAP as {}...".format(GMAIL_USER))
        try:
            mail = imaplib.IMAP4_SSL(IMAP_HOST)
            mail.login(GMAIL_USER, app_pass)
        except imaplib.IMAP4.error as exc:
            raise CommandError("IMAP login failed: {}".format(exc))

        # Select the Sent folder
        status, _ = mail.select('"{}"'.format(SENT_LABEL), readonly=True)
        if status != "OK":
            raise CommandError("Could not select Sent Mail folder.")

        status, data = mail.search(None, "ALL")
        if status != "OK":
            raise CommandError("Could not list Sent Mail.")

        all_ids = data[0].split()
        scan_ids = list(
            reversed(all_ids[-limit:] if len(all_ids) > limit else all_ids)
        )
        self.stdout.write(
            "  Sent folder: {} emails -- scanning {}".format(
                len(all_ids), len(scan_ids)
            )
        )

        # 4. Scan, parse, match
        to_import = []
        skipped_no_match = 0
        skipped_dup = 0
        skipped_date = 0

        for uid in scan_ids:
            s2, msg_data = mail.fetch(uid, "(RFC822)")
            if s2 != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            to_addr = _bare_addr(_decode_hdr(msg.get("To", "")))
            subject = _decode_hdr(msg.get("Subject", "")).strip()
            sent_dt = _parse_date(msg.get("Date", ""))
            body = _plain_body(msg).strip()
            cc = _decode_hdr(msg.get("Cc", "")).strip()

            if since_date and sent_dt and sent_dt < since_date:
                skipped_date += 1
                continue

            if to_addr not in inq_map:
                skipped_no_match += 1
                continue

            if (to_addr, subject) in existing:
                skipped_dup += 1
                continue

            best = sorted(inq_map[to_addr], key=lambda x: x["id"], reverse=True)[0]
            to_import.append({
                "inquiry_id": best["id"],
                "inquiry_name": best["name"],
                "to_email": to_addr,
                "subject": subject,
                "body": body,
                "cc": cc,
                "sent_dt": sent_dt,
            })
            existing.add((to_addr, subject))

        mail.logout()

        # 5. Summary
        self.stdout.write("-" * 65)
        self.stdout.write("  Matched (to import): {}".format(len(to_import)))
        self.stdout.write("  No inquiry match:    {}".format(skipped_no_match))
        self.stdout.write("  Duplicates skipped:  {}".format(skipped_dup))
        if since_date:
            self.stdout.write("  Before --since:      {}".format(skipped_date))
        self.stdout.write("-" * 65)

        if not to_import:
            self.stdout.write(self.style.WARNING("Nothing new to import."))
            return

        for m in to_import:
            s = (
                m["sent_dt"].strftime("%Y-%m-%d %H:%M")
                if m["sent_dt"] else "?"
            )
            self.stdout.write(
                "{:<34}{:<38}{:<22}#{} {}".format(
                    m["to_email"][:33],
                    m["subject"][:37],
                    s,
                    m["inquiry_id"],
                    m["inquiry_name"],
                )
            )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "[DRY RUN] {} records would be imported. No DB changes.".format(
                        len(to_import)
                    )
                )
            )
            return

        # 6. Write to DB
        self.stdout.write("Writing {} records to InquiryReply...".format(len(to_import)))
        objs = [
            InquiryReply(
                inquiry_id=m["inquiry_id"],
                sent_by=None,
                to_email=m["to_email"],
                cc=m["cc"],
                subject=m["subject"],
                body=m["body"],
            )
            for m in to_import
        ]
        with transaction.atomic():
            created_objs = InquiryReply.objects.bulk_create(objs)

        # Patch sent_at (auto_now_add cannot be overridden on create)
        for m, obj in zip(to_import, created_objs):
            if m["sent_dt"]:
                InquiryReply.objects.filter(pk=obj.pk).update(
                    sent_at=m["sent_dt"]
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Done. {} InquiryReply records backfilled successfully.".format(
                    len(created_objs)
                )
            )
        )
