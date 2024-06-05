import asyncio, numpy as np

async def fetch_data(delay: int,) -> np.ndarray:
    print(f"Fetching data with delay: {delay}")
    await asyncio.sleep(delay)
    return np.random.rand(3)

async def main():
    data = await fetch_data(1)
    print(data)