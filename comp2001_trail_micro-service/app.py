from config import connex_app, db

if __name__ == "__main__":
    connex_app.add_api(
        "swagger.yml",
        base_path="/api",  # or remove/change this as needed
        options={"swagger_ui": True},
        arguments={"title": "Trail Application REST API"},
    )

    connex_app.run(host="0.0.0.0", port=8000)
