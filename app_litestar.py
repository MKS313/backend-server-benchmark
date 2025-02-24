from datetime import datetime
import uvicorn
from litestar import Litestar, Request, Response, get
from litestar.logging import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
# import models
import models_dc as models
import config as cfg
from create_order import create_order, create_order_dc

# Define a logging configuration that suppresses lower-level logs
logging_config = LoggingConfig(
    root={"level": "CRITICAL"},  # Set level to ERROR to suppress INFO logs
)
logging_middleware_config = LoggingMiddlewareConfig()


@get("/")
async def root(request: Request) -> Response:
    # tic = time.time()

    resp = Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        content=await create_order_dc(),
    )

    # # toc = time.time()
    # elapsed_time = time.time() - tic
    # print(f"Elapsed time: {elapsed_time} seconds")

    return resp

# @get("/")
# async def root() -> str:
#     return "Hello, World!"


app = Litestar(
    logging_config=logging_config,
    route_handlers=[root],
    debug=False,
)

if __name__ == "__main__":
    # ab -n 20000 -c 10 http://127.0.0.1:8903/
    # oha --insecure -c 100 -n 50000 http://127.0.0.1:8903
    host = 'http://127.0.0.1'
    port = 8903
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    uvicorn.run(app="app_litestar:app", host="0.0.0.0", port=port, workers=cfg.num_workers, log_level="warning")
