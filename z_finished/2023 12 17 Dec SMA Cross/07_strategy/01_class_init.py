import numpy as np
import plotly.graph_objects as go

from logging import getLogger
from typing import NamedTuple

from quantfreedom.helper_funcs import cart_product
from quantfreedom.indicators.tv_indicators import sma_tv
from quantfreedom.enums import CandleBodyType
from quantfreedom.strategies.strategy import Strategy

logger = getLogger("info")


class IndicatorSettingsArrays(NamedTuple):
    sma_fast_length: np.array
    sma_slow_length: np.array


class SMACrossing(Strategy):
    def __init__(
        self,
        long_short: str,
        sma_fast_length: np.array,
        sma_slow_length: np.array,
    ) -> None:
        self.long_short = long_short

        cart_arrays = cart_product(
            IndicatorSettingsArrays(
                sma_fast_length=sma_fast_length,
                sma_slow_length=sma_slow_length,
            )
        )

        sma_fast_length = cart_arrays[0].astype(np.int_)
        sma_slow_length = cart_arrays[1].astype(np.int_)

        sma_bools = sma_fast_length < sma_slow_length

        self.indicator_settings_arrays: IndicatorSettingsArrays = IndicatorSettingsArrays(
            sma_fast_length=sma_fast_length[sma_bools],
            sma_slow_length=sma_slow_length[sma_bools],
        )

        if long_short == "long":
            self.set_entries_exits_array = self.long_set_entries_exits_array
            self.log_indicator_settings = self.long_log_indicator_settings
            self.entry_message = self.long_entry_message
        else:
            self.set_entries_exits_array = self.short_set_entries_exits_array
            self.log_indicator_settings = self.short_log_indicator_settings
            self.entry_message = self.short_entry_message

    