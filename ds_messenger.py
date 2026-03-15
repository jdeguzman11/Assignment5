# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# ds_messenger.py

"""Classes for sending/receiving messages from DS server."""

import socket
import time
import ds_protocol


class DirectMessage:
    """Represents a direct message."""

    def __init__(self, recipient=None, message=None, timestamp=None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    """Handles direct messaging with the DS server."""

    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def send(self, message: str, recipient: str) -> bool:
        """Sends a direct message."""
        pass

    def retrieve_new(self) -> list:
        """Retrieves new direct messages."""
        pass

    def retrieve_all(self) -> list:
        """Retrieves all direct messages."""
        pass

    def _connect(self):
        """Connect to the DS server and return a socket."""
        try:
            host, port = self.dsuserver
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            return sock

        except Exception:
            return None
