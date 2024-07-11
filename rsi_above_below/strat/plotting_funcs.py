import numpy as np

from quantfreedom import FootprintCandlesTuple
import plotly.graph_objects as go


def plotting_signals(
    candles: FootprintCandlesTuple,
    entry_signals: np.ndarray,
    rsi: np.ndarray,
    rsi_above_below: int,
):
    datetimes = candles.candle_open_datetimes

    fig = go.Figure()
    fig.add_scatter(
        x=datetimes,
        y=rsi,
        name="rsi",
        line_color="yellow",
    )
    fig.add_scatter(
        x=datetimes,
        y=entry_signals,
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
    )
    fig.add_hline(
        y=rsi_above_below,
        opacity=0.3,
        line_color="red",
    )
    fig.update_layout(
        height=500,
        xaxis_rangeslider_visible=False,
    )
    fig.show()
