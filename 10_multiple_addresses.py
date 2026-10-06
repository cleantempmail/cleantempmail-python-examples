"""Create a few test inboxes and inspect each once; no unbounded polling."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.count <= 10:
        parser.error("--count must be between 1 and 10")
    client = CleanTempMailClient.from_env()
    addresses = [client.generate_email() for _ in range(args.count)]
    for address in addresses:
        print(address, "messages:", len(client.get_emails(address, summary=True)))
    print(f"Used {2 * args.count} protected requests.")


if __name__ == "__main__":
    run(main)
