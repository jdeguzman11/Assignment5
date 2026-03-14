# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# ds_protocol.py

"""Functions for creating and parsing JSON messages from the DS server."""

import json
from collections import namedtuple

DataTuple = namedtuple("DataTuple", ["type", "token"])
MessageTuple = namedtuple(
    "MessageTuple", ["message", "from_user", "timestamp"]
    )


def extract_json(json_msg: str) -> DataTuple:
    """Utility functions for handling DS server JSON responses."""
    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj["response"]["type"]
        token = json_obj["response"].get("token", "")

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple(None, None)

    except (KeyError, TypeError):
        return DataTuple(None, None)

    return DataTuple(response_type, token)


def extract_direct_messages(json_msg: str) -> list[MessageTuple]:
    """Extracts messages from a JSON response from the DS server."""
    try:
        json_obj = json.loads(json_msg)
        messages = json_obj["response"].get("messages", [])

        extracted_messages = []
        for item in messages:
            message = item["message"]
            from_user = item["from"]
            timestamp = item["timestamp"]
            extracted_messages.append(
                MessageTuple(message, from_user, timestamp)
            )

        return extracted_messages

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return []

    except (KeyError, TypeError):
        return []


def create_direct_message(
        token: str, entry: str, recipient: str, timestamp: str
) -> str:
    """Create JSON string to send a direct message."""
    message_dict = {
        "token": token,
        "directmessage": {
            "entry": entry,
            "recipient": recipient,
            "timestamp": timestamp
        }
    }

    return json.dumps(message_dict)


def create_get_new(token: str) -> str:
    """Create JSON string that requests new direct messages."""
    message_dict = {
        "token": token,
        "directmessage": "new"
    }

    return json.dumps(message_dict)


def create_get_all(token: str) -> str:
    """Create JSON string that requests all direct messages."""
    message_dict = {
        "token": token,
        "directmessage": "all"
    }

    return json.dumps(message_dict)
