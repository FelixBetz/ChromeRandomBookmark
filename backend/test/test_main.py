"""test bookmarks.py"""
import json
import os
from ..app import create_app
from ..project.bookmark_parser import Bookmarks, date_from_webkit
from ..project.bookmarks import parse_urls, parse_folders


def test_bookmark_get():
    """test bookmarks api reuquest"""
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/bookmarks')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert isinstance(json_data["folders"], list)
        assert isinstance(json_data["urls"], list)


def test_parse_to_dict():
    """test parse_folders and parse_urls"""
    bookmarks = Bookmarks(os.path.join("test", "test_bookmark.json"))

    folders = parse_folders(bookmarks)

    assert folders[0]["name"] == "test"
    assert folders[0]["url_ids"] == [9, 8]

    assert folders[1]["name"] == "suboflder"
    assert folders[1]["url_ids"] == [12]

    url = parse_urls(bookmarks)[1]
    assert url["date_added"] == date_from_webkit(
        "13309819625972240").timestamp()

    assert url["id"] == 9
    assert url["name"] == "YouTube"
    assert url["url"] == "https://www.youtube.com/"
    assert url["date_last_used"] == 0
