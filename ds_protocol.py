# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# ds_protocol.py

"""Functions for creating and parsing JSON messages from the DS server."""

import json
from collections import namedtuple

DataTuple = namedtuple(
    "DataTuple", ["type", "message", "token"]
    )
MessageTuple = namedtuple(
    "MessageTuple",
    ["type", "messages"]
    )


def extract_json(json_msg: str) -> DataTuple:
    """Utility functions for handling DS server JSON responses."""
    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj["response"]["type"]
        message = json_obj["repsonse"]["message"]
        token = json_obj["response"].get("token", "")

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple(None, None)

    except (KeyError, TypeError):
        return DataTuple(None, None)

    return DataTuple(response_type, message, token)


def extract_direct_messages(json_msg: str):
    """Extracts messages from a JSON response from the DS server."""
    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj["response"]["type"]
        messages = json_obj["response"]["messages"]

        return MessageTuple(response_type, messages)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return []

    except (KeyError, TypeError):
        return []
