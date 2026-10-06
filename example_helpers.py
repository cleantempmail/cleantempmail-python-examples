"""Shared CLI handling; API failures always produce a non-zero exit status."""

import sys
from datetime import datetime, timezone

from cleantempmail import APIError, CleanTempMailError


def run(main):
    try:
        main()
    except APIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if exc.quota_exhausted:
            print("Quota exhausted. Check 11_key_usage.py; use another key or wait for a daily reset.", file=sys.stderr)
        elif exc.retry_after is not None:
            print(f"Retry after at least {exc.retry_after:g} seconds.", file=sys.stderr)
        raise SystemExit(1)
    except (CleanTempMailError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        raise SystemExit(130)


def display_email(message):
    print(f"ID: {message['id']}\nFrom: {message['from_address']}\nTo: {message['email_address']}")
    print(f"Subject: {message['subject']}")
    print("Time:", datetime.fromtimestamp(message["timestamp"], timezone.utc).isoformat())
    print(message.get("content", ""))
    for attachment in message.get("attachments", []):
        print(f"Attachment: {attachment['id']} · {attachment['filename']} · {attachment['size']} bytes")
