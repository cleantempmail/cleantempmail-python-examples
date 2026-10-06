"""Download attachment bytes to an explicit path, without overwriting files."""
import argparse
from pathlib import Path
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email_id")
    parser.add_argument("attachment_id", help="attachments[].id from get_email(email_id)")
    parser.add_argument("output", type=Path, help="Choose a path; do not trust an email-provided filename")
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Output already exists; choose a new path")
    data = CleanTempMailClient.from_env().download_attachment(args.email_id, args.attachment_id)
    with args.output.open("xb") as output:
        output.write(data)
    print(f"Saved {len(data)} bytes to {args.output}")


if __name__ == "__main__":
    run(main)
