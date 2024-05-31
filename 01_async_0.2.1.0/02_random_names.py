from random import randint
from time import perf_counter, sleep
from asyncio import gather, run, sleep as async_sleep

# The highest Pokemon id
MAX_POKEMON = 898
NAMES = [
    "jay",
    "jim",
    "roy",
    "axel",
    "billy",
    "charlie",
    "jax",
    "gina",
    "paul",
    "ringo",
    "ally",
    "nicky",
    "cam",
    "ari",
    "trudie",
    "cal",
    "carl",
    "lady",
    "lauren",
    "ichabod",
    "arthur",
    "ashley",
    "drake",
    "kim",
    "julio",
    "lorraine",
    "floyd",
    "janet",
    "lydia",
    "charles",
    "pedro",
    "bradley",
]


def get_random_name() -> str:
    name_id = randint(0, len(NAMES) - 1)
    name = NAMES[name_id]
    sleep(0.5)
    return name


async def get_random_name_async() -> str:
    name_id = randint(0, len(NAMES) - 1)
    name = NAMES[name_id]
    await async_sleep(1)
    return name


async def main() -> None:

    # synchronous call
    time_before = perf_counter()
    for _ in range(8):
        print(get_random_name())
    print(f"Total time (synchronous): {perf_counter() - time_before}" + "\n")

    # asynchronous call
    time_before = perf_counter()
    print(await gather(*[get_random_name_async() for _ in range(8)]))
    print(f"Total time (asynchronous): {perf_counter() - time_before}")


run(main())
