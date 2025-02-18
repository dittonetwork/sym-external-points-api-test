import pytest
import requests
from typing import Optional, Dict

from config_data import TestConfig


class ExternalPointsAPIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.request(method=method, url=url, params=params)
        return response

    def health_check(self) -> requests.Response:
        return self._make_request("GET", "/health")

    def get_last_block(self) -> requests.Response:
        return self._make_request("GET", "/last_block")

    def get_points_for_address(self, receiver_type: str, receiver_address: str, block_number: int) -> requests.Response:
        endpoint = f"/{receiver_type}/{receiver_address}"
        params = {"block_number": block_number}
        return self._make_request("GET", endpoint, params)

    def get_stats(self, block_number: int, receiver_type: Optional[str] = None) -> requests.Response:
        params = {"block_number": block_number}
        if receiver_type:
            params["receiver_type"] = receiver_type
        return self._make_request("GET", "/stats", params)

    def get_all_points(self, block_number: int, offset: int, limit: int,
                       receiver_type: Optional[str] = None) -> requests.Response:
        params = {
            "block_number": block_number,
            "offset": offset,
            "limit": limit
        }
        if receiver_type:
            params["receiver_type"] = receiver_type
        return self._make_request("GET", "/all", params)


@pytest.fixture
def api_client():
    return ExternalPointsAPIClient(TestConfig.API_BASE_URL)

