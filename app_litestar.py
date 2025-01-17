from datetime import datetime
import uvicorn
from litestar import Litestar, Request, get
from litestar.logging import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
# import models
import models_dc as models


# Define a logging configuration that suppresses lower-level logs
logging_config = LoggingConfig(
    root={"level": "CRITICAL"},  # Set level to ERROR to suppress INFO logs
)
logging_middleware_config = LoggingMiddlewareConfig()


single_orders = []
for k in range(10000):
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

resp_json = resp_#.model_dump_json()


@get("/")
async def root() -> models.Responses:
    """Keeping the tradition alive with hello world."""

    return resp_json

app = Litestar(
    logging_config=logging_config,
    route_handlers=[root],
    debug=False,
)

if __name__ == "__main__":
    host = 'http://127.0.0.1'
    port = 8903
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    uvicorn.run(app="app_litestar:app", host="0.0.0.0", port=port, workers=8, log_config=None)

