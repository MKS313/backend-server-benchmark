from datetime import datetime
from typing import List
from pydantic import BaseModel
from robyn import Request, Response, SubRouter, Config, Robyn
import models
# import models_dc as models
import config as cfg
import time


class Order(BaseModel):
    symbol: str
    instrument_id: str
    side: str
    volume: int
    start_time: str
    end_time: str


## insted Responses
class OrdersPage(BaseModel):
    number: int
    size: int
    content: List[Order]


# router = SubRouter(__file__, prefix="/api")

router = SubRouter(__file__)


@router.get("/")
async def root(request: Request) -> Response:
    tic = time.time()
    # page_size = 10
    # orders = [
    #     Order(
    #         symbol=str(k),
    #         instrument_id=str(k),
    #         side="buy",
    #         volume=50,
    #         start_time=datetime.now().isoformat(timespec="milliseconds"),
    #         end_time=datetime.now().isoformat(timespec="milliseconds"),
    #     )
    #     for k in range(10)
    # ]

    single_orders = []
    for k in range(cfg.num_order):
        single_orders.append(
            models.Order(
                symbol=str(k),
                instrument_id=str(k),
                side='buy',
                volume=50,
                start_time=datetime.now().isoformat(timespec='milliseconds'),
                end_time=datetime.now().isoformat(timespec='milliseconds'),
            )
        )

    # toc = time.time()
    elapsed_time = time.time() - tic
    print(f"Elapsed time: {elapsed_time} seconds")

    return Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        description=models.Orders(single=single_orders).model_dump_json(),
    )


#
rcfg = Config()
rcfg.processes = 8  # 10
rcfg.workers = 8  # 20
# rcfg.fast = True

app = Robyn(__file__, config=rcfg)
app.include_router(router)


if __name__ == "__main__":
    # ab -n 20000 -c 10 http://127.0.0.1:8902/
    # create a configured "Session" class

    # python app.py --processes 1 --workers 20

    host = 'http://127.0.0.1'
    port = 8902
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    app.start(host="0.0.0.0", port=port)
