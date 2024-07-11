import numpy as np
from os.path import join, abspath

from quantfreedom import FootprintCandlesTuple, Strategy

from rsi_above_below.strat.helper_class import StratHelpers
from rsi_above_below.strat.plotting_funcs import plotting_signals
from rsi_above_below.strat.dos_ind_cart_funcs import get_cur_ind_set_tuple, get_og_ind_and_dos_tuples
from rsi_above_below.strat.tuples_and_variables import (
    IndicatorSettings,
    static_os_tuple,
    exchange_settings_tuple,
    backtest_settings_tuple,
)

from logging import getLogger

logger = getLogger()


class RSIBelowAbove(Strategy):
    cur_ind_set_tuple: IndicatorSettings
    entry_signals: np.ndarray
    og_ind_set_tuple: IndicatorSettings
    rsi: np.ndarray
    rsi_above_below: int

    def __init__(
        self,
        rsi_length: np.ndarray,
        shuffle_bool: bool,
        rsi_above: np.ndarray = np.array([0]),
        rsi_below: np.ndarray = np.array([0]),
    ):
        self.log_folder = abspath(join(abspath(""), ".."))

        self.static_os_tuple = static_os_tuple
        self.exchange_settings_tuple = exchange_settings_tuple
        self.backtest_settings_tuple = backtest_settings_tuple

        self.strat_helpers = StratHelpers()

        ind_set_tuple = IndicatorSettings(
            rsi_above=rsi_above,
            rsi_below=rsi_below,
            rsi_length=rsi_length,
        )

        (
            self.og_dos_tuple,
            self.og_ind_set_tuple,
            self.total_dos,
            self.total_indicator_settings,
        ) = get_og_ind_and_dos_tuples(
            ind_set_tuple=ind_set_tuple,
            shuffle_bool=shuffle_bool,
        )

        self.total_filtered_settings = self.og_ind_set_tuple.rsi_length.size

        logger.debug("set_og_ind_and_dos_tuples")

    def set_cur_ind_set_tuple(
        self,
        set_idx: int,
    ):
        new_set_idx = self.get_settings_index(set_idx)

        self.cur_ind_set_tuple = get_cur_ind_set_tuple(
            set_idx=new_set_idx,
            og_ind_set_tuple=self.og_ind_set_tuple,
        )

    def plot_signals(
        self,
        candles: FootprintCandlesTuple,
    ):
        plotting_signals(
            candles=candles,
            entry_signals=self.entry_signals,
            rsi=self.rsi,
            rsi_above_below=self.rsi_above_below,
        )
