import uvicorn

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, model_validator, field_validator

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Hello World",
                "description": "A very nice Item",
                "price": -35.4,
            }
        }

    # @field_validator("price")
    # @classmethod
    # def price_must_be_positive(cls, value):
    #     if value < 0:
    #         raise ValueError("Price must be positive")
    #     return value

    @model_validator(mode="after")
    def checker(self):
        self.price
        return self


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    item_dict = item.model_dump()
    return {"item": item_dict}


if __name__ == "__main__":
    uvicorn.run(
        "testing:app",
        reload=True,
        reload_delay=0.25,
    )