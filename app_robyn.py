import json

from robyn import Request, Response, SubRouter, Config, Robyn, jsonify, WebSocket
import config as cfg
from create_order import create_order, create_order_sync

# router = SubRouter(__file__, prefix="/api")

doc = create_order_sync()

router = SubRouter(__file__)


# @router.get("/")
# async def root(request: Request) -> Response:
#     # # tic = time.time()
#
#     resp = Response(
#         status_code=200,
#         headers={"Content-Type": "application/json"},
#         description=await create_order(),
#     )
#
#     # # toc = time.time()
#     # elapsed_time = time.time() - tic
#     # print(f"Elapsed time: {elapsed_time} seconds")
#
#     return resp


# @router.get("/")
# async def root():
#     return "Hello, World!"


@router.get("/")
async def root():
    return json.loads(doc.model_dump_json())

#
rcfg = Config()
rcfg.processes = cfg.num_processes
rcfg.workers = cfg.num_workers
# rcfg.fast = True

app = Robyn(__file__, config=rcfg)
# app = Robyn(__file__)
app.include_router(router)

websocket = WebSocket(app, "/ws")


@websocket.on("connect")
def connect():
    return "Connected to ws"


@websocket.on("close")
def close():
    return "Goodbye world, from ws"


@websocket.on("message")
def message():
    return "Hello world, from ws"


if __name__ == "__main__":
    # ab -n 20000 -c 10 http://127.0.0.1:8902/
    # create a configured "Session" class

    # oha --no-tui --insecure -c 100 -n 50000 http://127.0.0.1:8902
    # oha --insecure -c 100 -n 50000 http://127.0.0.1:8902
    # python app_robyn.py --processes 20 --workers 20 --log-level WARN
    # python app_robyn.py --processes 8 --workers 8 --log-level WARN

    host = 'http://127.0.0.1'
    port = 8902
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    app.start(host="0.0.0.0", port=port)
