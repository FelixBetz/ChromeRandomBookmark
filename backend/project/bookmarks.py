"""handels the flask backend"""
import os
from flask import jsonify, Blueprint
from .bookmark_parser import Bookmarks

paths = [
    os.path.expanduser("~/.config/google-chrome/Default/Bookmarks"),
    os.path.expanduser(
        "~/Library/Application Support/Google/Chrome/Default/Bookmarks"),
    os.path.expanduser(
        "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks")
]

bookmark_routes = Blueprint('bookmark_routes', __name__)


@bookmark_routes.route("/api/bookmarks", methods=["GET"])
def get_bookmarks():
    """returns all bookmarks"""
    bookmark_instance = None
    for path in paths:
        if os.path.exists(path):
            bookmark_instance = Bookmarks(path)

    ret_folders = []
    ret_urls = []

    if bookmark_instance is not None:
        for folder in bookmark_instance.folders:
            element = {}
            element["name"] = folder.name
            url_ids = []
            for url in folder.urls:
                url_ids.append(int(url.id))
            element["url_ids"] = url_ids

            ret_folders.append(element)

        for url in bookmark_instance.urls:
            element = {}
            element["name"] = url.name
            element["id"] = int(url.id)
            element["url"] = url.url
            element["date_added"] = url.added.timestamp()
            try:
                element["date_last_used"] = url.modified.timestamp()
            except AttributeError:
                element["date_last_used"] = 0
            ret_urls.append(element)

    return jsonify({"folders": ret_folders, "urls": ret_urls})
