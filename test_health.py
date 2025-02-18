def test_health_check(api_client):
    response = api_client.health_check()
    assert response.status_code == 200