import numpy as np

from quantfreedom import FootprintCandlesTuple

from rsi_above_below.strat.rsi_above_below_class import RSIBelowAbove


class LongRSIBelowAbove(RSIBelowAbove):
    def get_long_or_short(self):
        return "long"

    def set_entries_exits_array(
        self,
        candles: FootprintCandlesTuple,
    ):
        self.rsi_above_below = self.cur_ind_set_tuple.rsi_below
        self.rsi = self.strat_helpers.get_rsi(
            candle_close_prices=candles.candle_close_prices,
            rsi_length=self.cur_ind_set_tuple.rsi_length,
        )

        self.entries = self.rsi < self.cur_ind_set_tuple.rsi_below

        self.entry_signals = np.where(self.entries, self.rsi, np.nan)

        self.exit_prices = np.full_like(self.entries, np.nan)


Long_Strat = LongRSIBelowAbove(
    rsi_below=np.arange(60, 19, -10),
    rsi_length=np.arange(14, 30, 5),
    shuffle_bool=False,
)
