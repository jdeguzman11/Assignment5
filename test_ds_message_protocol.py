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


def test_extract_direct_messages():
    """Unit test for JSON response from a direct message."""
    json_msg = '''
    {"response": {"type": "ok", "messages":[
        {"message": "Hello", "from": "markb", "timestamp": "111"},
        {"message": "SWE", "from": "jdawg", "timestamp": "711"}
    ]}}
    '''

    messages = ds_protocol.extract_direct_messages(json_msg)

    assert len(messages) == 2
    assert messages[0].message == "Hello"
    assert messages[0].from_user == "markb"
    assert messages[0].timestamp == "111"
    assert messages[1].message == "SWE"
    assert messages[1].from_user == "jdawg"
    assert messages[1].timestamp == "711"


def test_create_direct_message():
    """Unit test for creating a JSON string for sending direct message."""
    token = "example_token"
    msg = ds_protocol.create_direct_message(
        token, "SWE", "jdawg", "711"
    )

    assert '"token": "example_token"' in msg
    assert '"entry": "SWE"' in msg
    assert '"recipient": "jdawg"' in msg
    assert '"timestamp": "711"' in msg


def test_create_get_new():
    """Unit test for creating JSON string for requesting new messages."""
    token = "example_token"
    msg = ds_protocol.create_get_new(token)

    assert '"directmessage": "new"' in msg
