"""contains all tests for the file bookmark_parser.py"""
from datetime import datetime
from ..project.bookmark_parser import Bookmarks, date_from_webkit


def test_invalid_file():
    """create bookmark with invalid path"""
    bookmarks = Bookmarks("")
    assert bookmarks
    assert not bookmarks.urls
    assert not bookmarks.folders
    assert isinstance(bookmarks.folders, list)
    assert isinstance(bookmarks.urls, list)


def test_valid_file():
    """test with test_bookmark.json"""
    bookmarks = Bookmarks("test\\test_bookmark.json")

    # test urls
    assert len(bookmarks.urls) == 4
    assert isinstance(bookmarks.urls, list)

    assert bookmarks.urls[0].added == date_from_webkit("13309819596265629")
    assert isinstance(bookmarks.urls[0].added, datetime)

    assert bookmarks.urls[0].modified is None
    assert bookmarks.urls[0].id == "6"
    assert bookmarks.urls[0].name == "Hall – Wikipedia"
    assert bookmarks.urls[0].type == "url"
    assert bookmarks.urls[0].url == "https://de.wikipedia.org/wiki/Hall"

    # test folders
    assert len(bookmarks.folders) == 2
    assert isinstance(bookmarks.folders, list)

    assert bookmarks.folders[0].added == date_from_webkit("13309819607668907")
    assert isinstance(bookmarks.folders[0].added, datetime)

    assert bookmarks.folders[0].modified == date_from_webkit(
        "13309970147636799")
    assert isinstance(bookmarks.folders[0].modified, datetime)

    assert bookmarks.folders[0].id == "7"
    assert bookmarks.folders[0].name == "test"
    assert bookmarks.folders[0].type == "folder"
    assert bookmarks.folders[0].url == ""


def test_convert_timestamp():
    """test date_from_webkit(timestamp)"""
    test_dates = [
        13170147422089597,
        13150297844686316,
        13115171381595644,
    ]

    compare_dates = [
        datetime(2018, 5, 7, 6, 17, 2, 89597),
        datetime(2017, 9, 19, 12, 30, 44, 686316),
        datetime(2016, 8, 8, 23, 9, 41, 595644),
        datetime(1601, 8, 1, 1, 1, 0, 0),

    ]

    for i, date in enumerate(test_dates):
        assert date_from_webkit(date) == compare_dates[i]
