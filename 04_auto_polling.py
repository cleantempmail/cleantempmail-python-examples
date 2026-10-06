"""Poll summaries with a deadline, backoff and duplicate suppression."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import run


def auto_poll(email_address, duration_minutes=2, interval=10):
    client = CleanTempMailClient.from_env()
    print("Each inbox poll costs 1 request. Existing messages are shown once.")
    for message in client.iter_new_emails(email_address, timeout=duration_minutes * 60, interval=interval):
        print(f"{message['id']} · {message['from_address']} · {message['subject']}")
    print("Monitoring completed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("--timeout", type=float, default=120, help="Maximum monitoring time in seconds")
    parser.add_argument("--interval", type=float, default=10, help="Seconds between polls")
    args = parser.parse_args()
    auto_poll(args.email, args.timeout / 60, args.interval)


if __name__ == "__main__":
    run(main)
