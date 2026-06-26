"""
fetch_sent_replies.py
─────────────────────
Reads the Sent folder of propertism.tamil@gmail.com via IMAP
and matches sent emails against inquiry email addresses in the DB.

Requirements:
  - Gmail App Password (not your regular password)
  - Enable IMAP in Gmail settings → See All Settings → Forwarding and POP/IMAP

Usage (run from project root):
  python scripts/fetch_sent_replies.py
  python scripts/fetch_sent_replies.py --json

Environment variables needed:
  GMAIL_USER     = propertism.tamil@gmail.com
  GMAIL_APP_PASS = <16-char app password from Google Account>

To generate a Gmail App Password:
  1. Go to https://myaccount.google.com/security
  2. Enable 2-Step Verification if not already enabled
  3. Go to https://myaccount.google.com/apppasswords
  4. Create an app password for "Mail"
  5. Set as GMAIL_APP_PASS env var (or hardcode below for one-off use)
"""

import email
import imaplib
import json
import os
import sys
from email.header import decode_header

# ── Config ────────────────────────────────────────────────────────────────────

GMAIL_USER = os.environ.get("GMAIL_USER", "propertism.tamil@gmail.com")
GMAIL_APP_PASS = os.environ.get("GMAIL_APP_PASS", "")   # Must be set
IMAP_HOST = "imap.gmail.com"
SENT_FOLDER = '"[Gmail]/Sent Mail"'  # Gmail's sent folder label

# How many sent messages to fetch (most recent first)
FETCH_LIMIT = 200


def decode_mime_words(s):
    """Decode encoded email headers."""
    if not s:
        return ""
    parts = decode_header(s)
    decoded = []
    for part, encoding in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return " ".join(decoded)


def get_body(msg):
    """Extract plain-text body from email message."""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in disp:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")
    return ""


def fetch_sent_emails():
    """Connect to Gmail IMAP and return list of sent email dicts."""
    if not GMAIL_APP_PASS:
        print("ERROR: GMAIL_APP_PASS env var not set.", file=sys.stderr)
        print("  Set it with: set GMAIL_APP_PASS=xxxx-xxxx-xxxx-xxxx", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to {IMAP_HOST} as {GMAIL_USER}...")
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(GMAIL_USER, GMAIL_APP_PASS)
    mail.select(SENT_FOLDER, readonly=True)

    status, data = mail.search(None, "ALL")
    if status != "OK":
        print("Failed to list sent messages", file=sys.stderr)
        return []

    message_ids = data[0].split()
    print(f"Total sent messages in mailbox: {len(message_ids)}")

    # Take the most recent FETCH_LIMIT messages (newest first)
    recent_ids = message_ids[-FETCH_LIMIT:] if len(message_ids) > FETCH_LIMIT else message_ids
    recent_ids = list(reversed(recent_ids))

    results = []
    for uid in recent_ids:
        status, msg_data = mail.fetch(uid, "(RFC822)")
        if status != "OK":
            continue

        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        to_addr = decode_mime_words(msg.get("To", ""))
        subject = decode_mime_words(msg.get("Subject", ""))
        date_str = msg.get("Date", "")
        body = get_body(msg)

        results.append({
            "to": to_addr,
            "subject": subject,
            "date": date_str,
            "body_preview": body[:500].strip(),
        })

    mail.logout()
    return results


def match_with_inquiries(sent_emails):
    """
    Cross-reference sent emails with inquiry email addresses.
    Requires Django setup to access the DB.
    """
    try:
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        django.setup()
        from properties.models import Inquiry

        all_inquiries = list(Inquiry.objects.values("id", "email", "name", "status"))
        inquiry_email_map = {}
        for inq in all_inquiries:
            key = inq["email"].lower()
            if key not in inquiry_email_map:
                inquiry_email_map[key] = []
            inquiry_email_map[key].append(inq)

        print(f"Loaded {len(all_inquiries)} inquiries from DB ({len(inquiry_email_map)} unique emails)")

        matched = []
        unmatched = []

        for sent in sent_emails:
            to_clean = sent["to"].strip().lower()
            # Handle "Name <email>" format
            if "<" in to_clean:
                to_clean = to_clean.split("<")[-1].rstrip(">").strip()

            if to_clean in inquiry_email_map:
                inqs = inquiry_email_map[to_clean]
                sent["matched_inquiries"] = inqs
                matched.append(sent)
            else:
                unmatched.append(sent)

        return matched, unmatched

    except Exception as e:
        print(f"Django not available or DB error: {e}", file=sys.stderr)
        print("Returning all sent emails without matching.", file=sys.stderr)
        return sent_emails, []


if __name__ == "__main__":
    dump_json = "--json" in sys.argv

    sent = fetch_sent_emails()
    print(f"Fetched {len(sent)} sent emails\n")

    matched, unmatched = match_with_inquiries(sent)

    if dump_json:
        output = {
            "matched_count": len(matched),
            "unmatched_count": len(unmatched),
            "matched": matched,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*110}")
        print(f"  {len(matched)} sent emails matched to inquiry email addresses")
        print(f"  {len(unmatched)} sent emails had no matching inquiry")
        print(f"{'='*110}")
        print(f"\n{'To':<35} {'Subject':<40} {'Date':<32} {'Inq IDs'}")
        print("-" * 110)
        for m in matched:
            inq_ids = ", ".join(str(i["id"]) for i in m.get("matched_inquiries", []))
            print(
                f"{m['to'][:33]:<35} "
                f"{m['subject'][:38]:<40} "
                f"{m['date'][:30]:<32} "
                f"#{inq_ids}"
            )
