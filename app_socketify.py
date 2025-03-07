import asyncio
from socketify import App
import config as cfg
from create_order import create_order, create_order_sync


doc = create_order_sync()


async def root(res, req):
    orders_response = await create_order()

    # Send the response
    res.write_status(200)  # HTTP 200 OK
    res.write_header("Content-Type", "application/json")  # Set content type
    res.end(orders_response)  # Send JSON response


def run(app: App):
    # app.get("/", root)

    # app.get(
    #     "/",
    #     lambda res, req: res.end("Hello, World!")
    # )

    app.get(
        "/",
        lambda res, req: res.end(doc)
    )


if __name__ == "__main__":
    # oha --no-tui --insecure -c 100 -n 50000 http://127.0.0.1:8905
    # oha --insecure -c 100 -n 50000 http://127.0.0.1:8905
    # python -m socketify app_socketify:run --port 8905 --workers 20

    app = App()
    app.listen(8905, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))
    app.get("/", root)
    app.run()
