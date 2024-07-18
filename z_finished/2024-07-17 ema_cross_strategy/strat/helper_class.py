import numpy as np

from quantfreedom.indicators.tv_indicators import ema_tv

from logging import getLogger

logger = getLogger()


class StratHelpers:

    def get_first_second_emas(
        self,
        candle_close_prices: np.ndarray,
        first_ema_length: int,
        second_ema_length: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        
        first_ema_not_rounded = ema_tv(
            source=candle_close_prices,
            length=first_ema_length,
        )

        first_ema = np.around(first_ema_not_rounded, 2)

        first_ema_p = np.roll(first_ema, 1)
        first_ema_p[0] = np.nan

        second_ema_not_rounded = ema_tv(
            source=candle_close_prices,
            length=second_ema_length,
        )

        second_ema = np.around(second_ema_not_rounded, 2)

        second_ema_p = np.roll(second_ema, 1)
        second_ema_p[0] = np.nan
        
        return first_ema, first_ema_p, second_ema, second_ema_p
