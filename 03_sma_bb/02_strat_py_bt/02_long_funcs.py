import os
import numpy as np
from numpy.core.multiarray import array as array
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

    #######################################################
    #######################################################
    #######################################################
    ##################      Long     ######################
    ##################      Long     ######################
    ##################      Long     ######################
    #######################################################
    #######################################################
    #######################################################

    def long_set_entries_exits_array(
        self,
        candles: np.array,
        ind_set_index: int,
    ):
        try:
            self.rsi_is_below = self.indicator_settings_arrays.rsi_is_below[ind_set_index]
            self.rsi_length = self.indicator_settings_arrays.rsi_is_below[ind_set_index]
            self.current_ind_settings = IndicatorSettingsArrays(
                rsi_is_above=np.nan, rsi_is_below=self.rsi_is_below, rsi_length=self.rsi_length
            )

            rsi = rsi_tv(
                source=candles[: CandleBodyType.Close],
                length=self.rsi_length,
            )

            self.rsi = np.around(rsi, 1)
            logger.info(f"Created RSI rsi_length= {self.rsi_length}")

            prev_rsi = np.roll(self.rsi, 1)
            prev_rsi[0] = np.nan

            prev_prev_rsi = np.roll(prev_rsi, 1)
            prev_prev_rsi[0] = np.nan

            falling = prev_prev_rsi > prev_rsi
            rising = self.rsi > prev_rsi
            is_below = self.rsi < self.rsi_is_below

            self.entries = np.where(is_below & falling & rising, True, False)
            self.entry_signals = np.where(self.entries, self.rsi, np.nan)

            self.exit_prices = np.full_like(self.rsi, np.nan)
        except Exception as e:
            logger.error(f"Exception long_set_entries_exits_array -> {e}")
            raise Exception(f"Exception long_set_entries_exits_array -> {e}")

    def long_log_indicator_settings(
        self,
        ind_set_index: int,
    ):
        logger.info(
            f"Indicator Settings\
        \nIndicator Settings Index= {ind_set_index}\
        \nrsi_length= {self.rsi_length}\
        \nrsi_is_below= {self.rsi_is_below}"
        )

    def long_entry_message(
        self,
        bar_index: int,
    ):
        logger.info("\n\n")
        logger.info(
            f"Entry time!!! {self.rsi[bar_index-2]} > {self.rsi[bar_index-1]} < {self.rsi[bar_index]} and {self.rsi[bar_index]} < {self.rsi_is_below}"
        )
        
    #######################################################
    #######################################################
    #######################################################
    ##################      short    ######################
    ##################      short    ######################
    ##################      short    ######################
    #######################################################
    #######################################################
    #######################################################