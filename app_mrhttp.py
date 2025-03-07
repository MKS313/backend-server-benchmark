import mrhttp
import config as cfg
from create_order import create_order, create_order_sync


doc = create_order_sync()

app = mrhttp.Application()


# @app.route("/")
# def root(r) -> str:
#     # # tic = time.time()
#
#     # resp = Response(
#     #     status_code=200,
#     #     headers={"Content-Type": "application/json"},
#     #     content=await create_order(),
#     # )
#
#     # # toc = time.time()
#     # elapsed_time = time.time() - tic
#     # print(f"Elapsed time: {elapsed_time} seconds")
#
#     return create_order_sync()


# @app.route('/')
# def root(r) -> str:
#   return "Hello, World!"

@app.route('/', _type='json')
def root(r) -> str:
  return doc.model_dump_json()


if __name__ == '__main__':
    # https://github.com/MarkReedZ/mrhttp
    # execute this command in terminal

    # oha --insecure -c 100 -n 50000 http://127.0.0.1:8900

    host = 'http://127.0.0.1'
    port = 8900
    r = f'{host}:{port}'
    docs = r + '/docs'
    print(r)
    print(docs)

    app.run(host="0.0.0.0", port=port, cores=cfg.num_processes)


