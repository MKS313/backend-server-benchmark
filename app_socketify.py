from socketify import App

app = App()

app.get(
    "/",
    lambda res, req: res.end("Hello, World!")
)


if __name__ == "__main__":
    # oha --no-tui --insecure -c 100 -n 50000 http://127.0.0.1:8905

    app.listen(8905, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))

    app.run()



