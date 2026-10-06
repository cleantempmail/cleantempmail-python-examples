"""Use the reusable client in your own application."""
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    client = CleanTempMailClient.from_env()
    address = client.generate_email(prefix="qa.user")
    print("Address:", address)
    for message in client.get_emails(address):
        print(message["id"], message["subject"])
    print("Remaining quota:", client.get_usage()["remaining_total"])


if __name__ == "__main__":
    run(main)
