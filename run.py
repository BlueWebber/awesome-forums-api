from app import create_app
from config import config
from waitress import serve

app = create_app(config)


if __name__ == "__main__":
    # app.run(host="0.0.0.0")
    serve(app, host='0.0.0.0', port=5000)
