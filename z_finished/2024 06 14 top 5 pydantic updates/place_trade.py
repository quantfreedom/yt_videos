import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, model_validator
from quantfreedom.exchanges import Mufex
from my_keys import MufexKeys
from time import sleep

app = FastAPI()

Mufex_Test_Neo = Mufex(
    api_key=MufexKeys.mainnet_testacc_api_key,
    secret_key=MufexKeys.mainnet_testacc_secret_key,
    use_testnet=False,
)


class Item(BaseModel):
    asset_size: float
    sl_price: float
    tp_price: float

    class Config:
        json_schema_extra = {
            "example": {
                "asset_size": 0.005,
                "sl_price": 68400,
                "tp_price": 70400,
            }
        }

    @model_validator(mode="after")
    def checker(self):
        for field, value in self.model_dump().items():
            if value < 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"{field} must be positive. It is {value}",
                )
        return self


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    symbol = "BTCUSDT"

    order_id = Mufex_Test_Neo.create_long_hedge_mode_entry_market_order(
        asset_size=item.asset_size,
        symbol=symbol,
    )
    sleep(.2)
    sl_id = Mufex_Test_Neo.create_long_hedge_mode_sl_order(
        asset_size=item.asset_size,
        symbol=symbol,
        sl_price=item.sl_price,
    )
    sleep(.2)
    tp_id = Mufex_Test_Neo.create_long_hedge_mode_tp_limit_order(
        asset_size=item.asset_size,
        symbol=symbol,
        tp_price=item.tp_price,
    )

    return {"Order Id": order_id, "Stop loss": sl_id, "Take Profit Id": tp_id}


if __name__ == "__main__":
    uvicorn.run(
        "place_trade:app",
        reload=True,
        reload_delay=0.25,
    )
