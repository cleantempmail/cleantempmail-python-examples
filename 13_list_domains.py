"""Paginate public active domains (no key quota consumed)."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="")
    args = parser.parse_args()
    client = CleanTempMailClient.from_env()
    offset = 0
    while True:
        page = client.get_domains(q=args.query, limit=1000, offset=offset)
        for domain in page["domains"]:
            print(domain)
        offset += len(page["domains"])
        if not page["domains"] or offset >= page["total"]:
            break


if __name__ == "__main__":
    run(main)
