import numpy as np

from logging import getLogger

from quantfreedom import Strategy, DynamicOrderSettings

from ema_cross_strategy.strat.tuples_and_variables import IndicatorSettings, dos_tuple

logger = getLogger()


def get_og_ind_and_dos_tuples(
    ind_set_tuple: IndicatorSettings,
    shuffle_bool: bool,
) -> tuple[DynamicOrderSettings, IndicatorSettings]:

    og_strat = Strategy()

    cart_prod_array, total_dos = og_strat.get_ind_set_dos_cart_product(
        dos_tuple=dos_tuple,
        ind_set_tuple=ind_set_tuple,
    )

    filtered_cart_prod_array, total_indicator_settings = get_filter_cart_prod_array(
        cart_prod_array=cart_prod_array,
    )

    if shuffle_bool:
        rng = np.random.default_rng()
        final_cart_prod_array = rng.permutation(filtered_cart_prod_array, axis=1)
    else:
        final_cart_prod_array = filtered_cart_prod_array.copy()

    og_dos_tuple = og_strat.get_og_dos_tuple(
        final_cart_prod_array=final_cart_prod_array,
    )

    og_ind_set_tuple = get_og_ind_set_tuple(
        final_cart_prod_array=final_cart_prod_array,
    )
    return og_dos_tuple, og_ind_set_tuple, total_dos, total_indicator_settings


def get_og_ind_set_tuple(
    final_cart_prod_array: np.ndarray,
) -> IndicatorSettings:

    ind_set_tuple = IndicatorSettings(*tuple(final_cart_prod_array[12:]))
    logger.debug("ind_set_tuple")

    og_ind_set_tuple = IndicatorSettings(
        first_ema_length=ind_set_tuple.first_ema_length.astype(np.int_),
        second_ema_length=ind_set_tuple.second_ema_length.astype(np.int_),
    )
    logger.debug("og_ind_set_tuple")
    return og_ind_set_tuple


def get_filter_cart_prod_array(
    cart_prod_array: np.ndarray,
):
    filtered_cart_prod_array: np.ndarray
    total_indicator_settings = 1

    first_ema_col = 12
    second_ema_col = 13

    filtered_bools = cart_prod_array[first_ema_col] != cart_prod_array[second_ema_col]

    filtered_cart_prod_array = cart_prod_array[:, filtered_bools]
    logger.debug(f"cart prod size {cart_prod_array.shape[1]:,}")
    logger.debug(f"filtered cart prod size {filtered_cart_prod_array.shape[1]:,}")
    logger.debug(f"Removed {cart_prod_array.shape[1] -filtered_cart_prod_array.shape[1] }")

    filtered_cart_prod_array[11] = np.arange(filtered_cart_prod_array.shape[1])

    for array in filtered_cart_prod_array[12:]:
        total_indicator_settings *= np.unique(array).size
    logger.debug(f"Total Filted Order Settings: {total_indicator_settings}")

    return filtered_cart_prod_array, total_indicator_settings


def get_cur_ind_set_tuple(
    set_idx: int,
    og_ind_set_tuple: IndicatorSettings,
):
    cur_ind_set_tuple = IndicatorSettings(
        first_ema_length=og_ind_set_tuple.first_ema_length[set_idx],
        second_ema_length=og_ind_set_tuple.second_ema_length[set_idx],
    )
    logger.info(
        f"""
Indicator Settings
Indicator Settings Inex: {set_idx}
First EMA Length: {cur_ind_set_tuple.first_ema_length}
Second EMA Length: {cur_ind_set_tuple.second_ema_length}
            """
    )
    return cur_ind_set_tuple
