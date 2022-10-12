"""test bookmarks.py"""
import json
from ..app import create_app


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
