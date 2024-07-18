import numpy as np

from quantfreedom import FootprintCandlesTuple

from ema_cross_strategy.strat.ema_cross_class import EMACross


class LongEMACross(EMACross):
    def get_long_or_short(self):
        return "long"

    def set_entries_exits_array(
        self,
        candles: FootprintCandlesTuple,
    ):
        (
            self.first_ema,
            first_ema_p,
            self.second_ema,
            second_ema_p,
        ) = self.strat_helpers.get_first_second_emas(
            candle_close_prices=candles.candle_close_prices,
            first_ema_length=self.cur_ind_set_tuple.first_ema_length,
            second_ema_length=self.cur_ind_set_tuple.second_ema_length,
        )

        cur_first_above_second = self.first_ema > self.second_ema
        prev_first_below_second = first_ema_p < second_ema_p

        self.entries = cur_first_above_second & prev_first_below_second

        self.entry_signals = np.where(self.entries, self.first_ema, np.nan)

        self.exit_prices = np.full_like(self.second_ema, np.nan)


Long_Strat = LongEMACross(
    first_ema_length=np.arange(10, 301, 10),
    second_ema_length=np.arange(10, 301, 10),
    shuffle_bool=False,
)
