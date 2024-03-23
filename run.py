import flask
from app import create_app
from config import config

app = create_app(config)


@app.after_request
def apply_headers(response: flask.Response):
    response.headers['Access-Control-Allow-Origin'] = config.ALLOWED_ORIGINS
    response.headers["Access-Control-Allow-Methods"] = config.ALLOWED_METHODS
    response.headers["Access-Control-Allow-Headers"] = config.ALLOWED_HEADERS
    response.headers["Access-Control-Expose-Headers"] = config.EXPOSED_HEADERS
    response.headers["Content-Type"] = "application/json"
    return response


@app.errorhandler(404)
def page_not_found(e):
    return {"message": "resource doesn't exist"}, 404


if __name__ == "__main__":
    app.run()
