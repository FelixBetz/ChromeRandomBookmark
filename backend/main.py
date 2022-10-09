"""handels the flask backend"""
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
cors = CORS(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
