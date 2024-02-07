import os
import numpy as np
import plotly.graph_objects as go

from datetime import datetime
from logging import getLogger
from typing import NamedTuple

from quantfreedom.helper_funcs import cart_product
from quantfreedom.indicators.tv_indicators import rsi_tv
from quantfreedom.enums import CandleBodyType
from quantfreedom.strategies.strategy import Strategy


logger = getLogger("info")


class IndicatorSettingsArrays(NamedTuple):
    ema_length: np.array
    fast_length: np.array
    macd_below: np.array
    signal_smoothing: np.array
    slow_length: np.array


class RSIRisingFalling(Strategy):
    def __init__(
        self,
        long_short: str,
        ema_length: np.array,
        fast_length: np.array,
        macd_below: np.array,
        signal_smoothing: np.array,
        slow_length: np.array,
    ) -> None:
        self.long_short = long_short
        self.log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        cart_arrays = cart_product(
            named_tuple=IndicatorSettingsArrays(
                ema_length=ema_length,
                fast_length=fast_length,
                macd_below=macd_below,
                signal_smoothing=signal_smoothing,
                slow_length=slow_length,
            )
        )
        cart_arrays = cart_arrays.T[cart_arrays[1] < cart_arrays[4]].T
        self.indicator_settings_arrays: IndicatorSettingsArrays = IndicatorSettingsArrays(
            ema_length=cart_arrays[0].astype(np.int_),
            fast_length=cart_arrays[1].astype(np.int_),
            macd_below=cart_arrays[2].astype(np.int_),
            signal_smoothing=cart_arrays[3].astype(np.int_),
            slow_length=cart_arrays[4].astype(np.int_),
        )

        if long_short == "long":
            self.set_entries_exits_array = self.long_set_entries_exits_array
            self.log_indicator_settings = self.long_log_indicator_settings
            self.entry_message = self.long_entry_message
            self.live_evalutate = self.long_live_evaluate
            self.chart_title = "Long Signal"
        else:
            self.set_entries_exits_array = self.short_set_entries_exits_array
            self.log_indicator_settings = self.short_log_indicator_settings
            self.entry_message = self.short_entry_message
            self.live_evalutate = self.short_live_evaluate
            self.chart_title = "short Signal"
