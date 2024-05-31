from time import perf_counter, sleep
from asyncio import gather, run, sleep as async_sleep
from quantfreedom import dl_ex_candles, FootprintCandlesTuple, pretty_qf


def get_5m_candles() -> FootprintCandlesTuple:
    print("Getting 5m candles...")
    candles = dl_ex_candles(
        symbol="BTCUSDT",
        exchange="mufex",
        timeframe="5m",
        candles_to_dl=4500,
    )
    sleep(1)
    return candles


def get_30m_candles() -> FootprintCandlesTuple:
    print("Getting 30m candles...")
    candles = dl_ex_candles(
        symbol="BTCUSDT",
        exchange="mufex",
        timeframe="30m",
        candles_to_dl=3000,
    )
    sleep(1)
    return candles


def get_4h_candles() -> FootprintCandlesTuple:
    print("Getting 4h candles...")
    candles = dl_ex_candles(
        symbol="BTCUSDT",
        exchange="mufex",
        timeframe="4h",
        candles_to_dl=1500,
    )
    sleep(1)
    return candles


async def get_5m_candles_async() -> FootprintCandlesTuple:
    print("Getting 5m candles async ...")
    candles = dl_ex_candles(
        symbol="BTCUSDT",
        exchange="mufex",
        timeframe="5m",
        candles_to_dl=4500,
    )
    await async_sleep(1)
    return candles


async def get_30m_candles_async() -> FootprintCandlesTuple:
    print("Getting 30m candles async ...")
    candles = dl_ex_candles(
        symbol="BTCUSDT",
        exchange="mufex",
        timeframe="30m",
        candles_to_dl=3000,
    )
    await async_sleep(1)
    return candles


async def get_4h_candles_async() -> FootprintCandlesTuple:
    print("Getting 4h candles async ...")
    candles = dl_ex_candles(
        symbol="BTCUSDT",
        exchange="mufex",
        timeframe="4h",
        candles_to_dl=1500,
    )
    await async_sleep(1)
    return candles


async def main() -> None:

    # synchronous call
    time_before = perf_counter()
    pretty_qf(get_5m_candles())
    pretty_qf(get_30m_candles())
    pretty_qf(get_4h_candles())
    print(f"Total time (synchronous): {perf_counter() - time_before}" + "\n")

    # asynchronous call
    time_before = perf_counter()
    results = await gather(
        get_5m_candles_async(),
        get_30m_candles_async(),
        get_4h_candles_async(),
    )
    for result in results:
        pretty_qf(result)
    print(f"Total time (asynchronous): {perf_counter() - time_before}")


run(main())
