import pytest
from config_data import TestConfig
from utils import is_ethereum_address


class TestPointsDistribution:

    @pytest.mark.parametrize("receiver_type", ["staker", "network", "operator"])
    def test_get_points_valid_address(self, api_client, receiver_type):
        """Test points retrieval for valid address"""
        if receiver_type not in TestConfig.SUPPORTED_RECEIVER_TYPES:
            pytest.skip(f"Points for {receiver_type} are not supported")

        receiver_address =  TestConfig.RECEIVER_ADDRESSES.get(receiver_type)
        if receiver_address is None:
            pytest.fail(f"Receiver address for {receiver_type} is not provided")

        response = api_client.get_points_for_address(receiver_type, receiver_address, TestConfig.BLOCK_NUMBER)
        assert response.status_code == 200
        data = response.json()

        assert "receiver_address" in data, "receiver_address should be in response"
        assert data["receiver_address"] == receiver_address, "receiver_address should match"
        assert is_ethereum_address(data["receiver_address"]), "receiver_address should be a valid ethereum address"

        assert "receiver_type" in data, "receiver_type should be in response"
        assert data["receiver_type"] == receiver_type, "receiver_type should match"

        assert "block_number" in data, "block_number should be in response"
        assert data["block_number"] == TestConfig.BLOCK_NUMBER, "block_number should match"
        assert isinstance(data["block_number"], int), "block_number should be a integer"

        assert "points" in data, "points should be in response"
        assert isinstance(data["points"], list), "points should be a list"

        for point_entity in data["points"]:
            assert "points" in point_entity
            assert isinstance(point_entity["points"], int), "points should be a integer"
            assert point_entity["points"] > 0, "points should be greater than 0"

            assert "vault_address" in point_entity, "vault_address should be in response"
            assert is_ethereum_address(point_entity["vault_address"]), "vault_address should be a valid ethereum address"

            if TestConfig.POINTS_TYPE == "network":
                assert "network_address" in point_entity, "network_address should be in response"
                assert is_ethereum_address(point_entity["network_address"]), "operator_address should be a valid ethereum address"


    @pytest.mark.parametrize("receiver_type", ["staker", "network", "operator"])
    def test_get_points_invalid_address(self, api_client, receiver_type):
        """Test points retrieval for invalid address"""
        if receiver_type not in TestConfig.SUPPORTED_RECEIVER_TYPES:
            pytest.skip(f"Points for {receiver_type} are not supported")

        response = api_client.get_points_for_address(receiver_type, "invalid_address", TestConfig.BLOCK_NUMBER)
        assert response.status_code == 400

    @pytest.mark.parametrize("receiver_type", ["staker", "network", "operator"])
    def test_get_points_non_existent_address(self, api_client, receiver_type):
        """Test points retrieval for non-existent address"""
        if receiver_type not in TestConfig.SUPPORTED_RECEIVER_TYPES:
            pytest.skip(f"Points for {receiver_type} are not supported")

        non_existent = "0x0000000000000000000000000000000000000000"
        response = api_client.get_points_for_address(receiver_type, non_existent, TestConfig.BLOCK_NUMBER)
        assert len(response.json()["points"]) == 0, "Points list should be empty"