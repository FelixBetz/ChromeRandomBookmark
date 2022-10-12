"""handels the flask backend"""
from flask import jsonify, Blueprint


from . import bookmark_parser

bookmark_routes = Blueprint('bookmark_routes', __name__)


@bookmark_routes.route("/api/bookmarks", methods=["GET"])
def get_bookmarks():
    """returns all bookmarks"""

    ret_folders = []
    for folder in bookmark_parser.folders:
        element = {}
        element["name"] = folder.name
        url_ids = []
        for url in folder.urls:
            url_ids.append(int(url.id))
        element["url_ids"] = url_ids

        ret_folders.append(element)

    ret_urls = []
    for url in bookmark_parser.urls:
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
