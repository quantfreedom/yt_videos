import os
import numpy as np
from numpy.core.multiarray import array as array
import plotly.graph_objects as go

from datetime import datetime
from logging import getLogger
from typing import NamedTuple

from quantfreedom.helper_funcs import cart_product
from quantfreedom.indicators.tv_indicators import ema_tv
from quantfreedom.enums import CandleBodyType
from quantfreedom.strategies.strategy import Strategy


logger = getLogger("info")


class IndicatorSettingsArrays(NamedTuple):
    above_ema_bool: np.array
    ema_length: np.array
    falling_length: np.array


class EngulfingEMA(Strategy):
    def __init__(
        self,
        long_short: str,
        above_ema_bool: np.array,
        ema_length: np.array,
        falling_length: np.array,
    ) -> None:
        self.long_short = long_short
        self.log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        cart_arrays = cart_product(
            named_tuple=IndicatorSettingsArrays(
                above_ema_bool=above_ema_bool,
                ema_length=ema_length,
                falling_length=falling_length,
            )
        )

        self.indicator_settings_arrays: IndicatorSettingsArrays = IndicatorSettingsArrays(
            above_ema_bool=cart_arrays[0].astype(np.bool_),
            ema_length=cart_arrays[1].astype(np.int_),
            falling_length=cart_arrays[2].astype(np.int_),
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
            falling_length = self.indicator_settings_arrays.falling_length[ind_set_index] - 1

            open_prices = candles[:, CandleBodyType.Open]
            prev_open_prices = np.roll(open_prices, 1)
            prev_open_prices[0] = np.nan

            close_prices = candles[:, CandleBodyType.Close]
            prev_close_prices = np.roll(close_prices, 1)
            prev_close_prices[0] = np.nan

            current_green_candles = open_prices < close_prices

            close_diff = np.diff(close_prices, prepend=np.nan)

            red_candles = close_diff < 0

            falling_bools = np.full_like(close_diff, False, dtype=np.bool_)

            for x in range(falling_length, close_diff.size):
                if red_candles[x - falling_length : x + 1].all():
                    falling_bools[x] = True

            falling_bools = np.roll(falling_bools, 1)
            falling_bools[0] = False

            self.ema = ema_tv(source=close_prices, length=self.indicator_settings_arrays.ema_length[ind_set_index])

            if self.indicator_settings_arrays.above_ema_bool[ind_set_index]:
                above_below_bool = close_prices > self.ema
            else:
                above_below_bool = close_prices < self.ema

            bullish_engulfing_candles = (close_prices > prev_open_prices) & (open_prices <= prev_close_prices)

            self.entries = current_green_candles & bullish_engulfing_candles & falling_bools & above_below_bool

            self.entry_signals = np.where(self.entries, close_prices, np.nan)

            self.exit_prices = np.full_like(close_prices, np.nan)
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
        pass

    def short_log_indicator_settings(
        self,
        ind_set_index: int,
    ):
        pass

    def short_entry_message(
        self,
        bar_index: int,
    ):
        pass

    #######################################################
    #######################################################
    #######################################################
    ##################      Live     ######################
    ##################      Live     ######################
    ##################      Live     ######################
    #######################################################
    #######################################################
    #######################################################

    def live_set_indicator(
        self,
        ind_set_index: int,
    ):
        self.rsi_is_below = self.indicator_settings_arrays.rsi_is_below[ind_set_index]
        self.rsi_is_above = self.indicator_settings_arrays.rsi_is_above[ind_set_index]
        self.rsi_length = self.indicator_settings_arrays.rsi_length[ind_set_index]
        self.current_ind_settings = IndicatorSettingsArrays(
            rsi_is_above=self.rsi_is_above,
            rsi_is_below=self.rsi_is_below,
            rsi_length=self.rsi_length,
        )

        logger.info("live_set_ind_settings finished")

    def long_live_evaluate(
        self,
        candles: np.array,
    ):
        pass

    def short_live_evaluate(
        self,
        candles: np.array,
    ):
        pass

    #######################################################
    #######################################################
    #######################################################
    ##################      Plot     ######################
    ##################      Plot     ######################
    ##################      Plot     ######################
    #######################################################
    #######################################################
    #######################################################

    def plot_signals(
        self,
        candles: np.array,
    ):
        datetimes = candles[:, CandleBodyType.Timestamp].astype("datetime64[ms]")
        fig = go.Figure()
        fig.add_candlestick(
            x=datetimes,
            open=candles[:, 1],
            high=candles[:, 2],
            low=candles[:, 3],
            close=candles[:, 4],
            name="Candles",
        )
        fig.add_scatter(
            x=datetimes,
            y=self.ema,
            line_color="aqua",
        )
        fig.add_scatter(
            x=datetimes,
            y=self.entry_signals,
            name="Signals",
            mode="markers",
            marker=dict(
                size=12,
                symbol="hexagram",
                color="yellow",
                line=dict(
                    width=1,
                    color="DarkSlateGrey",
                ),
            ),
        )
        fig.update_layout(height=800, xaxis_rangeslider_visible=False)
        fig.show()

    def get_strategy_plot_filename(
        self,
        candles: np.array,
    ):
        # entry_filename = os.path.join(
        #     self.log_folder,
        #     "logs",
        #     "images",
        #     f'indicator_{datetime.utcnow().strftime("%m-%d-%Y_%H-%M-%S")}.png',
        # )
        # fig.write_image(entry_filename)
        # return entry_filename
        pass
