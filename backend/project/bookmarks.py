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


def parse_folders(arg_instance):
    """parse folders"""
    ret = []
    for folder in arg_instance.folders:
        element = {}
        element["name"] = folder.name
        url_ids = []
        for url in folder.urls:
            url_ids.append(int(url.id))
        element["url_ids"] = url_ids

        ret.append(element)

    return ret


def parse_urls(arg_instance):
    """parse urls"""
    ret = []
    for url in arg_instance.urls:
        element = {}
        element["name"] = url.name
        element["id"] = int(url.id)
        element["url"] = url.url
        element["date_added"] = url.added.timestamp()
        try:
            element["date_last_used"] = url.modified.timestamp()
        except AttributeError:
            element["date_last_used"] = 0
        ret.append(element)

    return ret


@bookmark_routes.route("/api/bookmarks", methods=["GET"])
def get_bookmarks():
    """returns all bookmarks"""
    bookmark_instance = Bookmarks(
        paths[2])

    ret_folders = []
    ret_urls = []

    if bookmark_instance is not None:
        ret_folders = parse_folders(bookmark_instance)
        ret_urls = parse_urls(bookmark_instance)

    return jsonify({"folders": ret_folders, "urls": ret_urls})
