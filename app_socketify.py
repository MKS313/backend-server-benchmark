import asyncio

from socketify import App

from datetime import datetime
from typing import List
from pydantic import BaseModel
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


async def root_handler(res, req):
    # tic = time.time()

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

    orders_response = models.Orders(single=single_orders).model_dump_json()

    # Send the response
    res.write_status(200)  # HTTP 200 OK
    res.write_header("Content-Type", "application/json")  # Set content type
    res.end(orders_response)  # Send JSON response


app = App()

app.get("/", root_handler)

# app.get(
#     "/",
#     lambda res, req: res.end("Hello, World!")
# )

if __name__ == "__main__":
    # oha --no-tui --insecure -c 100 -n 50000 http://127.0.0.1:8905
    # oha --insecure -c 100 -n 50000 http://127.0.0.1:8905

    app.listen(8905, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))

    app.run()
