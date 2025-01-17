from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import models
# import models_dc as models


app = FastAPI()


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

resp_json = resp_#.__dict__


@app.get("/", response_model=models.Responses)
async def root():
    return resp_json
    # return JSONResponse(resp_json)


# @app.get("/", response_model=models.Responses)
# async def root():
#     return resp_json
#     # return JSONResponse(resp_json)


# @app.get("/", response_model=str)
# async def root():
#     return "Hello, World!"
#     # return JSONResponse(resp_json)


if __name__ == '__main__':
    # execute this command in terminal
    # fastapi dev main.py

    host = 'http://127.0.0.1'
    port = 8901
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    # uvicorn.run(app="main:app", host="0.0.0.0", port=9000, reload=True, workers=4)
    uvicorn.run(app="app_fastapi:app", host="0.0.0.0", port=port, workers=8, log_config=None)




