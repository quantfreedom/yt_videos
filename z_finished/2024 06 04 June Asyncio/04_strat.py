from asyncio import gather, run, sleep as async_sleep
from quantfreedom.exchanges.mufex import Mufex

async def long_1m_candles_async():
    print("Getting long 1m candles...")
    await async_sleep(2)
    mufex_main = Mufex(use_testnet=False)
    mufex_main.get_candles(
        symbol="BTCUSDT",
        timeframe="1m",
    )
    await async_sleep(mufex_main.get_sleep_time_to_next_bar())
    print("Lomg 1m loop")
    while True:
        candles = mufex_main.get_candles(
            symbol="BTCUSDT",
            timeframe="1m",
        )
        red_candle = candles.candle_open_prices[-1] > candles.candle_close_prices[-1]
        if red_candle:
            print("Long Red 1 min candle. Time To trade")
        await async_sleep(mufex_main.get_sleep_time_to_next_bar())


async def short_1m_candles_async():
    print("Short 1m candle strat ...")
    await async_sleep(2)
    mufex_main = Mufex(use_testnet=False)
    mufex_main.get_candles(
        symbol="BTCUSDT",
        timeframe="1m",
    )
    await async_sleep(mufex_main.get_sleep_time_to_next_bar())
    print("Short 1m loop")
    while True:
        candles = mufex_main.get_candles(
            symbol="BTCUSDT",
            timeframe="1m",
        )
        green_candle = candles.candle_open_prices[-1] < candles.candle_close_prices[-1]
        if green_candle:
            print("Short 1 min green candle. Trade time baby!!!")
        await async_sleep(mufex_main.get_sleep_time_to_next_bar())


async def main() -> None:
    await gather(
        long_1m_candles_async(),
        short_1m_candles_async(),
    )


run(main())
