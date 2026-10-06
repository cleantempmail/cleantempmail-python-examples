"""Check remaining quota without consuming a request from the key."""
import json
from cleantempmail import CleanTempMailClient
from example_helpers import run


if __name__ == "__main__":
    run(lambda: print(json.dumps(CleanTempMailClient.from_env().get_usage(), indent=2)))
