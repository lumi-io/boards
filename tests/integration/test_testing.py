from api import create_app

def test_homepage():
    app = create_app(test_config=True)
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200