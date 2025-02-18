import re

def is_ethereum_address(value):
    return bool(re.fullmatch(r"0x[a-fA-F0-9]{40}", value))