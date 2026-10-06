"""Read an inbox. Failed requests are not displayed as an empty inbox."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import display_email, run


def get_emails(email_address):
    return CleanTempMailClient.from_env().get_emails(email_address)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    args = parser.parse_args()
    messages = get_emails(args.email)
    print(f"Messages: {len(messages)}")
    if not messages:
        print("Inbox is empty.")
    for message in messages:
        display_email(message)
        print()


if __name__ == "__main__":
    run(main)
