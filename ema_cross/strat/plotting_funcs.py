import numpy as np

from quantfreedom import FootprintCandlesTuple
import plotly.graph_objects as go


def plotting_signals(
    candles: FootprintCandlesTuple,
    entry_signals: np.ndarray,
    first_ema: np.ndarray,
    second_ema: np.ndarray,
):
    datetimes = candles.candle_open_datetimes

    fig = go.Figure()
    fig.add_candlestick(
        x=datetimes,
        open=candles.candle_open_prices,
        high=candles.candle_high_prices,
        low=candles.candle_low_prices,
        close=candles.candle_close_prices,
        name="Candles",
    )
    fig.add_scatter(
        x=datetimes,
        y=first_ema,
        name="First EMA",
        line=dict(color="yellow", width=3),
    )
    fig.add_scatter(
        x=datetimes,
        y=second_ema,
        name="Second EMA",
        line=dict(color="green", width=3),
    )
    fig.add_scatter(
        x=datetimes,
        y=entry_signals,
        name="Buy Signal",
        mode="markers",
        marker=dict(size=8, symbol="circle", color="#00F6FF"),
    )
    fig.update_layout(height=600, xaxis_rangeslider_visible=False)
    fig.show()
