import os
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from quantfreedom.enums import CandleBodyType
from quantfreedom.helper_funcs import dl_ex_candles, cart_product
from quantfreedom.indicators.tv_indicators import macd_tv, ema_tv
from quantfreedom.strategies.strategy import Strategy

from logging import getLogger
from typing import NamedTuple


logger = getLogger("info")


class IndicatorSettingsArrays(NamedTuple):
    signal_above_slow: np.array
    ema_fast_length: np.array
    ema_mid_length: np.array
    ema_slow_length: np.array


class EMACrossOver(Strategy):
    signal_above_slow = None
    ema_fast_length = None
    ema_mid_length = None
    ema_slow_length = None

    def __init__(
        self,
        long_short: str,
        signal_above_slow: np.array,
        ema_fast_length: np.array,
        ema_mid_length: np.array,
        ema_slow_length: np.array,
    ):
        self.long_short = long_short
        self.log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        cart_arrays = cart_product(
            named_tuple=IndicatorSettingsArrays(
                signal_above_slow=signal_above_slow,
                ema_fast_length=ema_fast_length,
                ema_mid_length=ema_mid_length,
                ema_slow_length=ema_slow_length,
            )
        )

        cart_arrays = cart_arrays.T[(cart_arrays[1] < cart_arrays[2]) & (cart_arrays[2] < cart_arrays[3])].T

        self.indicator_settings_arrays: IndicatorSettingsArrays = IndicatorSettingsArrays(
            signal_above_slow=cart_arrays[0].astype(np.bool_),
            ema_fast_length=cart_arrays[1].astype(np.int_),
            ema_mid_length=cart_arrays[2].astype(np.int_),
            ema_slow_length=cart_arrays[3].astype(np.int_),
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
            # datetimes = candles[:, CandleBodyType.Timestamp].astype("datetime64[ms]")
            # open_prices = candles[:, CandleBodyType.Open]
            high_prices = candles[:, CandleBodyType.High]
            low_prices = candles[:, CandleBodyType.Low]
            closing_prices = candles[:, CandleBodyType.Close]

            self.ema_fast_length = self.indicator_settings_arrays.ema_fast_length[ind_set_index]
            self.ema_mid_length = self.indicator_settings_arrays.ema_mid_length[ind_set_index]
            self.ema_slow_length = self.indicator_settings_arrays.ema_slow_length[ind_set_index]
            self.signal_above_slow = self.indicator_settings_arrays.signal_above_slow[ind_set_index]

            self.ema_fast = ema_tv(
                source=closing_prices,
                length=self.ema_fast_length,
            )
            self.ema_mid = ema_tv(
                source=closing_prices,
                length=self.ema_mid_length,
            )
            self.ema_slow = ema_tv(
                source=closing_prices,
                length=self.ema_slow_length,
            )

            prev_ema_fast = np.roll(self.ema_fast, 1)
            prev_ema_fast[0] = np.nan

            prev_ema_mid = np.roll(self.ema_mid, 1)
            prev_ema_mid[0] = np.nan

            fast_above_mid = self.ema_fast > self.ema_mid
            prev_fast_below_mid = prev_ema_fast < prev_ema_mid

            mid_above_slow = self.ema_mid > self.ema_slow
            low_prices_above_slow = low_prices > self.ema_slow

            mid_below_slow = self.ema_mid < self.ema_slow
            high_prices_below_slow = high_prices < self.ema_slow

            if self.signal_above_slow:
                self.entries = (
                    (fast_above_mid == True)
                    & (prev_fast_below_mid == True)
                    & (mid_above_slow == True)
                    & (low_prices_above_slow == True)
                )
            else:
                self.entries = (
                    (fast_above_mid == True)
                    & (prev_fast_below_mid == True)
                    & (mid_below_slow == True)
                    & (high_prices_below_slow == True)
                )

            self.entry_signals = np.where(self.entries, self.ema_fast, np.nan)

            self.exit_prices = np.full_like(self.entries, np.nan)

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
        \nema_length= {self.ema_length}\
        \nfast_length= {self.fast_length}\
        \nmacd_below= {self.macd_below}\
        \nsignal_smoothing= {self.signal_smoothing}\
        \nslow_length= {self.slow_length}"
        )

    def long_entry_message(
        self,
        bar_index: int,
    ):
        logger.info("\n\n")
        logger.info(f"Entry time!!!")

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
        fig = go.Figure()
        datetimes = candles[:, CandleBodyType.Timestamp].astype("datetime64[ms]")
        fig = make_subplots(
            cols=1,
            rows=2,
            shared_xaxes=True,
            subplot_titles=["Candles", "MACD"],
            row_heights=[0.6, 0.4],
            vertical_spacing=0.1,
        )
        # Candlestick chart for pricing
        fig.append_trace(
            go.Candlestick(
                x=datetimes,
                open=candles[:, CandleBodyType.Open],
                high=candles[:, CandleBodyType.High],
                low=candles[:, CandleBodyType.Low],
                close=candles[:, CandleBodyType.Close],
                name="Candles",
            ),
            col=1,
            row=1,
        )
        fig.append_trace(
            go.Scatter(
                x=datetimes,
                y=self.ema,
                name="EMA",
                line_color="yellow",
            ),
            col=1,
            row=1,
        )
        ind_shift = np.roll(self.histogram, 1)
        ind_shift[0] = np.nan
        colors = np.where(
            self.histogram >= 0,
            np.where(ind_shift < self.histogram, "#26A69A", "#B2DFDB"),
            np.where(ind_shift < self.histogram, "#FFCDD2", "#FF5252"),
        )
        fig.append_trace(
            go.Bar(
                x=datetimes,
                y=self.histogram,
                name="histogram",
                marker_color=colors,
            ),
            row=2,
            col=1,
        )
        fig.append_trace(
            go.Scatter(
                x=datetimes,
                y=self.macd,
                name="macd",
                line_color="#2962FF",
            ),
            row=2,
            col=1,
        )
        fig.append_trace(
            go.Scatter(
                x=datetimes,
                y=self.signal,
                name="signal",
                line_color="#FF6D00",
            ),
            row=2,
            col=1,
        )
        fig.append_trace(
            go.Scatter(
                x=datetimes,
                y=self.entry_signals,
                mode="markers",
                name="entries",
                marker=dict(
                    size=12,
                    symbol="circle",
                    color="#00F6FF",
                    line=dict(
                        width=1,
                        color="DarkSlateGrey",
                    ),
                ),
            ),
            row=2,
            col=1,
        )
        # Update options and show plot
        fig.update_layout(height=800, xaxis_rangeslider_visible=False)
        fig.show()
