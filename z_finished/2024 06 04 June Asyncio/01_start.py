from time import perf_counter, sleep
from asyncio import gather, run, sleep as async_sleep

def sleep_for(timer: int):
    print(f"Sleeping for {timer} seconds")
    sleep(timer)

async def sleep_for_async(timer: int):
    print(f"Async Sleeping for {timer} seconds")
    await async_sleep(timer)


async def main() -> None:
    # synchronous call
    time_before = perf_counter()
    for timer in range(1, 4):
        sleep_for(timer)
    print(f"Total time (synchronous): {perf_counter() - time_before}" + "\n")
    
    # asynchronous call
    time_before = perf_counter()
    await gather(*[sleep_for_async(timer) for timer in range(1, 4)])
    print(f"Total time (asynchronous): {perf_counter() - time_before}")
    
run(main())