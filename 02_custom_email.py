"""Choose an active domain, then generate a custom address."""
import argparse
from cleantempmail import CleanTempMailClient
from example_helpers import run


def generate_custom_email(prefix, domain=None):
    return CleanTempMailClient.from_env().generate_email(prefix=prefix, domain=domain)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", default="qa.user")
    parser.add_argument("--domain", help="Must appear in /api/domains; unavailable domains return HTTP 409")
    args = parser.parse_args()
    client = CleanTempMailClient.from_env()
    domain = args.domain
    if domain is None:
        domains = client.get_domains(limit=1)["domains"]
        if not domains:
            raise ValueError("No public active domains are available")
        domain = domains[0]
    print(client.generate_email(prefix=args.prefix, domain=domain))


if __name__ == "__main__":
    run(main)
