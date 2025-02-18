def test_get_last_block_success(api_client):
    response = api_client.get_last_block()
    assert response.status_code == 200
    data = response.json()
    assert "last_block_number" in data, "last_block_number should be in response"
    assert isinstance(data["last_block_number"], int), "last_block_number should be a integer"