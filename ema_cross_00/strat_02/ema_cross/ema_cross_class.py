import numpy as np
from os.path import join, abspath

from quantfreedom import FootprintCandlesTuple, Strategy

from ema_cross_00.strat_02.ema_cross.dos_ind_cart_funcs import get_og_ind_and_dos_tuples
from ema_cross_00.strat_02.ema_cross.tuples_and_variables import (
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

        ind_set_tuple = IndicatorSettings(
            first_ema_length=first_ema_length,
            second_ema_length=second_ema_length,
        )

        get_og_ind_and_dos_tuples(
            ind_set_tuple=ind_set_tuple,
            shuffle_bool=shuffle_bool,
        )
