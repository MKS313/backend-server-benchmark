from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Any, Union


@dataclass
class Asset:
    instrument_id: str
    volume: int


@dataclass
class ByPower:
    buy_power: float
    credit: float


@dataclass
class Portfolio:
    token: str
    id: str
    assets: List[Asset]
    buy_power: ByPower


@dataclass
class Order:
    symbol: str
    instrument_id: str
    side: str
    volume: int
    # value: float

    start_time: str
    end_time: str


@dataclass
class PairSignal:
    buy: List[Order]
    sell: List[Order]


@dataclass
class Orders:
    single: List[Order] = field(default_factory=list)
    pair: PairSignal = None
    multi_pair: Any = None


@dataclass
class Responses:
    id: str
    status: int
    message: str
    data: Any = None


@dataclass
class SimInput:
    token: str
    id: str
    date: datetime
