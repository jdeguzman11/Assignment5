# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# ds_messenger.py

"""Classes for sending/receiving messages from DS server."""


class DirectMessage:
    """Represents a direct message."""

    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """Handles direct messaging with the DS server."""

    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None

    def send(self, message: str, recipient: str) -> bool:
        """Sends a direct message."""
        pass

    def retrieve_new(self) -> list:
        """Retrieves new direct messages."""
        pass

    def retrieve_all(self) -> list:
        """Retrieves all direct messages."""
        pass
