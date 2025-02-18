class TestConfig:
    API_BASE_URL = "https://partner.url/external/api/"  # The base URL for the API.
    POINTS_TYPE= "network"   # The type of points, either "network" or "vault".
    SUPPORTED_RECEIVER_TYPES = ["staker", "operator"]  # A list of supported receiver types. ["staker", "network", "operator"]
    RECEIVER_ADDRESSES = {
        "staker": "0xa5188f25C9F02870E78F7fAF5cf4E3D2ff307eaa",
        "network": "0x123xxx",
        "operator": "0x123xxx",
    }  # A addresses for each supported receiver type
    BLOCK_NUMBER = 21872694  # The block number to use for tests.
