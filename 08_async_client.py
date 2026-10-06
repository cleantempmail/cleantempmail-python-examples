"""Run blocking HTTP calls with asyncio.to_thread; no aiohttp dependency."""
import asyncio
from cleantempmail import CleanTempMailClient
from example_helpers import run


async def generate_address():
    # Each task owns its client and usage snapshot. This demo makes 3 requests.
    return await asyncio.to_thread(CleanTempMailClient.from_env().generate_email)


async def main():
    tasks = [asyncio.create_task(generate_address()) for _ in range(3)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise result
        print(result)


if __name__ == "__main__":
    run(lambda: asyncio.run(main()))
