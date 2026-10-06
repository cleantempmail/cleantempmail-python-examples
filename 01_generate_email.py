"""Generate one random address (1 quota request)."""
from cleantempmail import CleanTempMailClient
from example_helpers import run


def generate_email():
    return CleanTempMailClient.from_env().generate_email()


if __name__ == "__main__":
    run(lambda: print(generate_email()))
