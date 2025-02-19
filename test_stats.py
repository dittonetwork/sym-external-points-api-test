import pytest
from config_data import TestConfig

class TestStats:
    def test_get_stats_success(self, api_client):
        """Test successful stats retrieval"""
        response = api_client.get_stats(TestConfig.BLOCK_NUMBER)
        assert response.status_code == 200
        data = response.json()
        assert "total_points" in data, "total_points should be in response"
        assert isinstance(data["total_points"], int), "total_points should be a integer"

        for receiver_type in TestConfig.SUPPORTED_RECEIVER_TYPES:
            assert receiver_type + "s" in data, f"{receiver_type} should be in response"
            assert isinstance(data[receiver_type + "s"], int), f"{receiver_type} should be a integer"

    @pytest.mark.parametrize("receiver_type", ["staker", "network", "operator"])
    def test_get_stats_with_receiver_type(self, api_client, receiver_type):
        """Test stats retrieval with receiver type filter"""
        if receiver_type not in TestConfig.SUPPORTED_RECEIVER_TYPES:
            pytest.skip(f"Points for {receiver_type} are not supported")

        response = api_client.get_stats(TestConfig.BLOCK_NUMBER, receiver_type)
        assert response.status_code == 200
        data = response.json()
        assert receiver_type + "s" in data, f"{receiver_type} should be in response"
        assert isinstance(data[receiver_type + "s"], int), f"{receiver_type} should be a integer"

