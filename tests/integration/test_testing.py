def test_homepage_with_fixture(test_client):
    response = test_client.get('/')
    assert response.status_code == 200