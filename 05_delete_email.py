"""Permanently delete one message, only when explicitly confirmed."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email_id", help="id returned by /api/emails")
    parser.add_argument("--yes", action="store_true", help="Confirm permanent deletion")
    args = parser.parse_args()
    if not args.yes:
        parser.error("No request sent. Add --yes to confirm permanent deletion.")
    CleanTempMailClient.from_env().delete_email(args.email_id)
    print("Message deleted.")


if __name__ == "__main__":
    run(main)
