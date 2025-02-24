import config as cfg
import models
import models_dc
from datetime import datetime

async def create_order() -> str:
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

    return models.Orders(single=single_orders).model_dump_json()


async def create_order_dc() -> models_dc.Orders:
    single_orders = []
    for k in range(cfg.num_order):
        single_orders.append(
            models_dc.Order(
                symbol=str(k),
                instrument_id=str(k),
                side='buy',
                volume=50,
                start_time=datetime.now().isoformat(timespec='milliseconds'),
                end_time=datetime.now().isoformat(timespec='milliseconds'),
            )
        )

    return models_dc.Orders(single=single_orders)


