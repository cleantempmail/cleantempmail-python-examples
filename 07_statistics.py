"""Get cached service statistics. Each call with a key consumes quota."""
import json
from cleantempmail import CleanTempMailClient
from example_helpers import run


def main():
    client = CleanTempMailClient.from_env()
    result = {
        "overview": client.get_statistics(),
        "last_24h": client.get_24h_distribution(),
        "top_subjects": client.get_top_subjects(),
        "top_domains": client.get_top_domains(),
        "top_senders": client.get_top_senders(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run(main)
