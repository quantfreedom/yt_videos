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
    rsi_is_above: np.array
    rsi_is_below: np.array
    rsi_length: np.array


class RSIRisingFalling(Strategy):
    def __init__(
        self,
        long_short: str,
        rsi_length: int,
        rsi_is_above: np.array = np.array([0]),
        rsi_is_below: np.array = np.array([0]),
    ) -> None:
        self.long_short = long_short
        self.log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        cart_arrays = cart_product(
            named_tuple=IndicatorSettingsArrays(
                rsi_is_above=rsi_is_above,
                rsi_is_below=rsi_is_below,
                rsi_length=rsi_length,
            )
        )

        self.indicator_settings_arrays: IndicatorSettingsArrays = IndicatorSettingsArrays(
            rsi_is_above=cart_arrays[0],
            rsi_is_below=cart_arrays[1],
            rsi_length=cart_arrays[2].astype(np.int_),
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
