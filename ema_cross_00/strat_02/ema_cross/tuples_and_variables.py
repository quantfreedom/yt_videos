import numpy as np

from typing import NamedTuple

from quantfreedom.core.enums import (
    BacktestSettings,
    ExchangeSettings,
    StaticOrderSettings,
    DynamicOrderSettings,
    IncreasePositionType,
    CandleBodyType,
    LeverageStrategyType,
    StopLossStrategyType,
    TakeProfitStrategyType,
    TrailingSLStrategyType,
)


class IndicatorSettings(NamedTuple):
    first_ema_length: np.ndarray
    second_ema_length: np.ndarray


backtest_settings_tuple = BacktestSettings()

exchange_settings_tuple = ExchangeSettings(
    asset_tick_step=3,
    leverage_mode=1,
    leverage_tick_step=2,
    limit_fee_pct=0.0003,
    market_fee_pct=0.0006,
    max_asset_size=100.0,
    max_leverage=150.0,
    min_asset_size=0.001,
    min_leverage=1.0,
    mmr_pct=0.004,
    position_mode=3,
    price_tick_step=1,
)

static_os_tuple = StaticOrderSettings(
    increase_position_type=IncreasePositionType.RiskPctAccountEntrySize,
    leverage_strategy_type=LeverageStrategyType.Dynamic,
    pg_min_max_sl_bcb="min",
    sl_strategy_type=StopLossStrategyType.SLBasedOnCandleBody,
    sl_to_be_bool=False,
    starting_bar=100,
    starting_equity=1000.0,
    static_leverage=None,
    tp_fee_type="limit",
    tp_strategy_type=TakeProfitStrategyType.RiskReward,
    trailing_sl_strategy_type=TrailingSLStrategyType.Nothing,
    z_or_e_type=None,
)

dos_tuple = DynamicOrderSettings(
    account_pct_risk_per_trade=np.array([5]),
    max_trades=np.array([2]),
    risk_reward=np.array([5, 10]),
    sl_based_on_add_pct=np.array([0.3, 0.5]),
    sl_based_on_lookback=np.array([30]),
    sl_bcb_type=np.array([CandleBodyType.Low]),
    sl_to_be_cb_type=np.array([CandleBodyType.Nothing]),
    sl_to_be_when_pct=np.array([0]),
    trail_sl_bcb_type=np.array([CandleBodyType.Nothing]),
    trail_sl_by_pct=np.array([0]),
    trail_sl_when_pct=np.array([0]),
)

# dos_tuple = DynamicOrderSettings(
#     account_pct_risk_per_trade=np.array([20]),
#     max_trades=np.array([2, 4, 6]),
#     risk_reward=np.array([3, 5, 10]),
#     sl_based_on_add_pct=np.array([0.3, 0.5, 1]),
#     sl_based_on_lookback=np.array([30]),
#     sl_bcb_type=np.array([CandleBodyType.Low]),
#     sl_to_be_cb_type=np.array([CandleBodyType.Nothing]),
#     sl_to_be_when_pct=np.array([0]),
#     trail_sl_bcb_type=np.array([CandleBodyType.Low]),
#     trail_sl_by_pct=np.array([2, 3, 4]),
#     trail_sl_when_pct=np.array([2, 3, 4]),
# )
