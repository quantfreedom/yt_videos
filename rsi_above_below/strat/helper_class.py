import numpy as np

from quantfreedom.indicators.tv_indicators import rsi_tv

from logging import getLogger

logger = getLogger()


class StratHelpers:

    def get_rsi(
        self,
        candle_close_prices: np.ndarray,
        rsi_length: int,
    ) -> np.ndarray:

        rsi_not_rounded = rsi_tv(
            source=candle_close_prices,
            length=rsi_length,
        )

        rsi = np.around(rsi_not_rounded, 2)

        return rsi
