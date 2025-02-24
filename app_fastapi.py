import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import config as cfg
from create_order import create_order


app = FastAPI()


@app.get("/")
async def root(request: Request) -> Response:
    # # tic = time.time()

    resp = Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        content=await create_order(),
    )

    # # toc = time.time()
    # elapsed_time = time.time() - tic
    # print(f"Elapsed time: {elapsed_time} seconds")

    return resp


# @app.get("/", response_model=models.Responses)
# async def root():
#     return resp_json
#     # return JSONResponse(resp_json)


# @app.get("/")
# async def root():
#     return "Hello, World!"


if __name__ == '__main__':
    # execute this command in terminal
    # fastapi dev main.py
    # ab -n 20000 -c 10 http://127.0.0.1:8901/

    # oha --insecure -c 100 -n 50000 http://127.0.0.1:8901

    host = 'http://127.0.0.1'
    port = 8901
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    # uvicorn.run(app="main:app", host="0.0.0.0", port=9000, reload=True, workers=4)
    uvicorn.run(app="app_fastapi:app", host="0.0.0.0", port=port, workers=cfg.num_workers, log_level="warning")




