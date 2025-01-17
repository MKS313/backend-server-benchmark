import json
from datetime import datetime
from robyn import Robyn
import models
# import models_dc as models
import config as cfg


app = Robyn(__file__)


#
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

resp_ = models.Responses(
    id='10',
    status=200,
    message='ok',
    data=models.Orders(single=single_orders)
)

resp_json = resp_.model_dump_json()


@app.get("/")
async def root():
    # return "Hello, World!"
    return resp_json

# @app.get("/")
# async def root():
#     single_orders = []
#     for k in range(cfg.num_order):
#         single_orders.append(
#             models.Order(
#                 symbol=str(k),
#                 instrument_id=str(k),
#                 side='buy',
#                 volume=50,
#                 start_time=datetime.now().isoformat(timespec='milliseconds'),
#                 end_time=datetime.now().isoformat(timespec='milliseconds'),
#             )
#         )
#
#     return models.Responses(
#         id='10',
#         status=200,
#         message='ok',
#         data=models.Orders(single=single_orders)
#     ).model_dump_json()


# @app.get("/")
# async def root():
#     return "Hello, World!"

if __name__ == "__main__":
    # ab -n 20000 -c 10 http://1270.0.1:8880/
    # create a configured "Session" class

    # python app.py --processes 1 --workers 20

    host = 'http://127.0.0.1'
    port = 8902
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    app.start(host="0.0.0.0", port=port)


