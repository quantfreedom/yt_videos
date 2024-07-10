import numpy as np
from os.path import join, abspath

from quantfreedom import FootprintCandlesTuple, Strategy

from ema_cross.strat.dos_ind_cart_funcs import get_cur_ind_set_tuple, get_og_ind_and_dos_tuples
from ema_cross.strat.helper_class import StratHelpers
from ema_cross.strat.plotting_funcs import plotting_signals
from ema_cross.strat.tuples_and_variables import (
    IndicatorSettings,
    static_os_tuple,
    exchange_settings_tuple,
    backtest_settings_tuple,
)

from logging import getLogger

logger = getLogger()


class EMACross(Strategy):
    entry_signals: np.ndarray
    second_ema: np.ndarray
    first_ema: np.ndarray
    cur_ind_set_tuple: IndicatorSettings
    og_ind_set_tuple: IndicatorSettings

    def __init__(
        self,
        first_ema_length: np.ndarray,
        second_ema_length: np.ndarray,
        shuffle_bool: bool,
    ):
        self.log_folder = abspath(join(abspath(""), ".."))

        self.static_os_tuple = static_os_tuple
        self.exchange_settings_tuple = exchange_settings_tuple
        self.backtest_settings_tuple = backtest_settings_tuple

        self.strat_helpers = StratHelpers()

        ind_set_tuple = IndicatorSettings(
            first_ema_length=first_ema_length,
            second_ema_length=second_ema_length,
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

        self.total_filtered_settings = self.og_ind_set_tuple.first_ema_length.size

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
            first_ema=self.first_ema,
            second_ema=self.second_ema,
        )
