"""Minimal demo; polling is opt-in and no messages are deleted."""
import argparse
import json
from cleantempmail import CleanTempMailClient
from example_helpers import display_email, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wait", action="store_true", help="Poll for up to 120 seconds (each poll consumes quota)")
    args = parser.parse_args()
    client = CleanTempMailClient.from_env()
    print("Key usage (this lookup is free):")
    print(json.dumps(client.get_usage(), indent=2))
    address = client.generate_email()
    print("Temporary address:", address)
    print("Messages:", len(client.get_emails(address, summary=True)))
    if args.wait:
        print("Send a test message to the address above. Checking every 10 seconds.")
        message = client.wait_for_email(address)
        if message:
            display_email(client.get_email(message["id"]))
        else:
            print("No message arrived before monitoring ended.")
    print("Latest charged-response usage:", json.dumps(client.last_usage))


if __name__ == "__main__":
    run(main)
