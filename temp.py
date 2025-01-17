from typing import List, Union, Any
from pydantic import BaseModel
from datetime import datetime

import uvicorn
from fastapi import FastAPI
import config as cfg


class Asset(BaseModel):
    # symbol: str
    instrument_id: str
    volume: int
    # price: float


class ByPower(BaseModel):
    buy_power: float
    credit: float


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


# ==================================
app = FastAPI()


single_orders = []
for k in range(10000):
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

resp_ = Responses(
    id='10',
    status=200,
    message='ok',
    data=Orders(single=single_orders)
)


@app.get("/", response_model=Responses)
async def root():
    return resp_


if __name__ == '__main__':
    # execute this command in terminal
    # fastapi dev main.py

    host = 'http://127.0.0.1'
    port = 8904
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    uvicorn.run(app="app_fastapi:app", host="0.0.0.0", port=port, workers=20, log_config=None)


