import json
from datetime import datetime
from robyn import Robyn, Config
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


rcfg = Config()
rcfg.processes = 10
rcfg.workers = 20
rcfg.fast = True

app = Robyn(__file__, config=rcfg)


@app.get("/")
async def root():
    single_orders = []
    for k in range(10):
        single_orders.append(
            Order(
                symbol=str(k),
                instrument_id=str(k),
                side='buy',
                volume=50,
                start_time=datetime.now().isoformat(timespec='milliseconds'),
                end_time=datetime.now().isoformat(timespec='milliseconds'),
            )
        )

    return Responses(
        id='10',
        status=200,
        message='ok',
        data=Orders(single=single_orders)
    ).model_dump_json()


if __name__ == "__main__":
    # python app.py --processes 1 --workers 20

    host = 'http://127.0.0.1'
    port = 8902
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    app.start(host="0.0.0.0", port=port)
