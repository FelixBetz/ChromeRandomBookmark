"""handels the flask backend"""
from flask_cors import CORS
from flask import Flask
import chrome_bookmarks


app = Flask(__name__)
cors = CORS(app)


if __name__ == "__main__":

    for folder in chrome_bookmarks.folders:
        print(folder.name)
        print(folder.folders)
    for url in chrome_bookmarks.urls:
        print(url.url, url.name)

    app.run(host="0.0.0.0", port=8080, debug=False)
