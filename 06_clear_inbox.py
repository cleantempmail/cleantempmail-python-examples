"""Permanently clear an inbox, only when explicitly confirmed."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("--yes", action="store_true", help="Confirm permanent deletion of this inbox's mail")
    args = parser.parse_args()
    if not args.yes:
        parser.error("No request sent. Add --yes to confirm clearing the inbox.")
    print("Deleted:", CleanTempMailClient.from_env().clear_inbox(args.email))


if __name__ == "__main__":
    run(main)
