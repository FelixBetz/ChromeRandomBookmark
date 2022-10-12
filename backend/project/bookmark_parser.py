"""parses chrome bookmarks"""
from datetime import datetime, timedelta
import json
import os


def date_from_webkit(timestamp):
    """converts epoch timestamp to unix timestamp"""
    epoch_start = datetime(1601, 1, 1)
    delta = timedelta(microseconds=int(timestamp))
    return epoch_start + delta


class Item(dict):
    """Item class, dict based. properties: `id`, `name`, `type`, `url`, `folders`, `urls`"""

    @property
    # pylint: disable=C0103
    def id(self):
        """returns id"""
        return self["id"]

    @property
    def name(self):
        """returns name"""
        return self["name"]

    @property
    def type(self):
        """returns url"""
        return self["type"]

    @property
    def url(self):
        """returns url"""
        if "url" in self:
            return self["url"]
        return ""

    @property
    def added(self):
        """returns added date"""
        return date_from_webkit(self["date_added"])

    @property
    def modified(self):
        """returns modified date"""
        if "date_modified" in self:
            return date_from_webkit(self["date_modified"])
        return None

    @property
    def urls(self):
        """returns urls"""
        items = []
        for children in self["children"]:
            if children["type"] == "url":
                items.append(Item(children))
        return items


class Bookmarks:
    """Bookmarks class. attrs: `path`. properties: `folders`, `urls`"""
    path = None

    def __init__(self, path):
        if not os.path.exists(path):
            self.urls = []
            self.folders = []
            return
        self.path = path
        with open(path, encoding="utf-8") as file:
            self.data = json.load(file)
        self.attr_list = self.process_roots()
        self.urls = self.attr_list["urls"]
        self.folders = self.attr_list["folders"]

    def process_roots(self):
        """process roots"""
        attr_list = {"urls": [], "folders": []}
        with open(self.path, encoding="utf-8") as file:
            roots_data = json.load(file)
        for _, value in roots_data["roots"].items():
            if "children" in value:
                self.process_tree(attr_list, value["children"])
        return attr_list

    def process_tree(self, attr_list, children_list):
        """process tree"""
        for item in children_list:
            self.process_urls(item, attr_list)
            self.process_folders(item, attr_list)

    def process_urls(self, item, attr_list):
        """process urls"""
        if "type" in item and item["type"] == "url":
            attr_list["urls"].append(Item(item))

    def process_folders(self, item, attr_list):
        """process folders"""
        if "type" in item and item["type"] == "folder":
            attr_list["folders"].append(Item(item))
            if "children" in item:
                self.process_tree(attr_list, item["children"])


paths = [
    os.path.expanduser("~/.config/google-chrome/Default/Bookmarks"),
    os.path.expanduser(
        "~/Library/Application Support/Google/Chrome/Default/Bookmarks"),
    os.path.expanduser(
        "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks")
]


folders = []
urls = []


for f in paths:
    if os.path.exists(f):
        instance = Bookmarks(f)
        folders = instance.folders
        urls = instance.urls
