# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# test_ds_message_protocol.py

"""Unit tests for ds_protocol file."""

import ds_protocol


def test_extract_json():
    """Unit test for handling valid JSON responses from DS server."""
    json_msg = '''
    {"response": {"type": "ok", "token": "example_token"}}
    '''

    result = ds_protocol.extract_json(json_msg)

    assert result.type == "ok"
    assert result.token == "example_token"


def test_extract_json_invalid():
    """Unit test for handling invalid JSON responses from DS server."""
    json_msg = "invalid json"

    result = ds_protocol.extract_json(json_msg)

    assert result.type is None
    assert result.token is None
