"""flask app"""

from flask import Flask

from .project import bookmarks


def create_app():
    """creates flask app"""
    app = Flask(__name__)

    app.register_blueprint(bookmarks.bookmark_routes)

    return app
