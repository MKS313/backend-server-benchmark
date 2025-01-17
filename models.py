from typing import List, Union, Any
from pydantic import BaseModel
from datetime import datetime


class Asset(BaseModel):
    # symbol: str
    instrument_id: str
    volume: int
    # price: float


class ByPower(BaseModel):
    buy_power: float
    credit: float


class Portfolio(BaseModel):
    token: str
    id: str
    assets: List[Asset]
    buy_power: ByPower


class Order(BaseModel):
    symbol: str
    instrument_id: str
    side: str
    volume: int
    # value: float

    start_time: str
    end_time: str


class PairSignal(BaseModel):
    buy: List[Order]
    sell: List[Order]


class Orders(BaseModel):
    # id: str
    single: List[Order] = None
    pair: PairSignal = None
    multi_pair: Any = None


class Responses(BaseModel):
    id: Union[str, None] = None
    status: int
    message: str
    data: Any = None


class SimInput(BaseModel):
    token: str
    id: str
    date: datetime


