import asyncio
import httpx
from datasets import load_dataset

DATASET_NAME = "imdb"
dataset = load_dataset(DATASET_NAME)

HOST = "localhost"
PORT = 7890
CONCURRENCY_LIMIT = 50


async def send(text: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore):
    url = f"http://{HOST}:{PORT}/api/v1/reviews/add"
    async with semaphore:
        try:
            response = await client.post(url, json={"text": text})
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send: {repr(e)}")


async def main():
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [
            send(sample["text"], client, semaphore)
            for sample in dataset["train"].select(range(1000))
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
