import os
import numpy as np
from numpy.core.multiarray import array as array
import plotly.graph_objects as go

from datetime import datetime
from logging import getLogger
from typing import NamedTuple

from quantfreedom.helper_funcs import cart_product
from quantfreedom.indicators.tv_indicators import sma_tv, bb_tv
from quantfreedom.enums import CandleBodyType
from quantfreedom.strategies.strategy import Strategy


logger = getLogger("info")


class IndicatorSettingsArrays(NamedTuple):
    sma_length: np.array
    sma_lookback: np.array
    bb_length: np.array
    bb_multi: np.array


class SMAandBB(Strategy):
    def __init__(
        self,
        long_short: str,
        sma_length: np.array,
        sma_lookback: np.array,
        bb_length: np.array,
        bb_multi: np.array,
    ) -> None:
        self.long_short = long_short
        self.log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        cart_arrays = cart_product(
            named_tuple=IndicatorSettingsArrays(
                sma_length=sma_length,
                sma_lookback=sma_lookback,
                bb_length=bb_length,
                bb_multi=bb_multi,
            )
        )

        self.indicator_settings_arrays: IndicatorSettingsArrays = IndicatorSettingsArrays(
            sma_length=cart_arrays[0].astype(np.int_),
            sma_lookback=cart_arrays[1].astype(np.int_),
            bb_length=cart_arrays[2].astype(np.int_),
            bb_multi=cart_arrays[3],
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
            self.rsi_length = self.indicator_settings_arrays.rsi_length[ind_set_index]
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

    def short_set_entries_exits_array(
        self,
        candles: np.array,
        ind_set_index: int,
    ):
        try:
            close_prices = candles[:, CandleBodyType.Close]
            
            self.sma_length = self.indicator_settings_arrays.sma_length[ind_set_index]
            self.sma_lookback = self.indicator_settings_arrays.sma_lookback[ind_set_index]
            self.bb_length = self.indicator_settings_arrays.bb_length[ind_set_index]
            self.bb_multi = self.indicator_settings_arrays.bb_multi[ind_set_index]
            
            self.sma = sma_tv(source=close_prices, length=self.sma_length)
            self.basic_bb, self.upper_bb, self.lower_bb = bb_tv(length=self.bb_length, multi=self.bb_multi, source=close_prices)

            down_trend = np.full_like(close_prices, False, dtype=np.bool_)
            for i in range(self.sma_lookback, self.sma.size):
                down_trend[i] = (self.sma[i - self.sma_lookback : i + 1] < close_prices[i - self.sma_lookback : i + 1]).all()
            
            bb_short_signals = close_prices > self.upper_bb
            
            self.entries = (down_trend == True) & (bb_short_signals == True)
            self.entry_signals = np.where(self.entries, close_prices, np.nan)

            self.exit_prices = np.full_like(self.rsi, np.nan)
        except Exception as e:
            logger.error(f"Exception short_set_entries_exits_array -> {e}")
            raise Exception(f"Exception short_set_entries_exits_array -> {e}")

    def short_log_indicator_settings(
        self,
        ind_set_index: int,
    ):
        logger.info(
            f"Indicator Settings\
        \nIndicator Settings Index= {ind_set_index}\
        \nrsi_length= {self.rsi_length}\
        \nrsi_is_above= {self.rsi_is_above}"
        )

    def short_entry_message(
        self,
        bar_index: int,
    ):
        logger.info("\n\n")
        logger.info(
            f"Entry time!!! {self.rsi[bar_index-2]} < {self.rsi[bar_index-1]} > {self.rsi[bar_index]} and {self.rsi[bar_index]} > {self.rsi_is_above}"
        )

    #######################################################
    #######################################################
    #######################################################
    ##################      Plot     ######################
    ##################      Plot     ######################
    ##################      Plot     ######################
    #######################################################
    #######################################################
    #######################################################
