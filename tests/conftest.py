import pytest
from flask_pymongo import PyMongo
from api import create_app

@pytest.fixture(scope="module")
def test_client():
    app = create_app(True)
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client