import pickle
from os import remove
from os.path import exists
from time import perf_counter
from time import gmtime, strftime
from quantfreedom.backtesters import run_df_backtest
from rsi_rising_falling import rsi_rising_falling_long_strat


if __name__ == "__main__":
    start = perf_counter()

    if exists("backtest_results.h5"):
        remove("backtest_results.h5")

    print("loading candles")
    candle_path = "../dbs/oct_dec_candles.pkl"
    with open(candle_path, "rb") as f:
        oct_dec_candles = pickle.load(f)

    backtest_results = run_df_backtest(
        candles=oct_dec_candles,
        strategy=rsi_rising_falling_long_strat,
        threads=32,
        num_chunk_bts=4000000,
        # step_by=6,
    )
    print("\n" + "Backtest results done now saving to hdf5")
    bt_results_path = "../dbs/backtest_results.h5"
    backtest_results.to_hdf(
        path_or_buf=bt_results_path,
        key="backtest_results",
        mode="w",
    )

    end = perf_counter()
    print(strftime("\n" + "It took %M mins and %S seconds to complete the backtest", gmtime(int(end - start))))
