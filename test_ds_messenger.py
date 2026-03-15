# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# test_ds_messenger.py

"""Unit tests for ds_messenger file."""

from ds_messenger import DirectMessage, DirectMessenger

import ds_protocol


def test_direct_message_init():
    """Testing DirectMessage initialization."""
    msg = DirectMessage("jdawg", "SWE", "711")

    assert msg.recipient == "jdawg"
    assert msg.message == "SWE"
    assert msg.timestamp == "711"


def test_direct_messenger_init():
    """Testing DirectMessenger initialization."""
    messenger = DirectMessenger(("clotho.ics.uci.edu, 2021"), "user", "pass")

    assert messenger.dsuserver == ("clotho.ics.uci.edu, 2021")
    assert messenger.username == "user"
    assert messenger.password == "pass"
    assert messenger.token is None


def test_connect_failure():
    """Testing _connect with failed connection."""
    messenger = DirectMessenger(("invalid", 2006), "user", "pass")

    assert messenger._connect() is None


def test_send_false():
    """Testing send returns false if connections fails."""
    messenger = DirectMessenger(("invalid", 2006), "user", "pass")

    assert messenger.send("SWE", "jdawg") is False


def test_retrieve_new_empty():
    """Test retrieve_new returns empty list if connection fails."""
    messenger = DirectMessenger(("invalid", 2006), "user", "pass")

    assert messenger.retrieve_new() == []


def test_retrieve_all_empty():
    """Test retrieve_all returns empty list if connection fails."""
    messenger = DirectMessenger(("invalid", 2006), "user", "pass")

    assert messenger.retrieve_all() == []


def test_recv_response_empty():
    """Test _recv_response handles empty response."""
    messenger = DirectMessenger(("clotho.ics.uci.edu, 2021"), "user", "pass")

    class FakeRecvFile:
        def readline(self):
            return ""

    result = messenger._recv_response(FakeRecvFile())

    assert result == ds_protocol.DataTuple(None, None)


def test_send_json_failure():
    """Testing _send_json returns false on write failure."""
    messenger = DirectMessenger(("clotho.ics.uci.edu, 2021"), "user", "pass")

    class FakeSendFile:
        def write(self, _):
            raise OSError("write failed")

        def flush(self):
            return None

    assert messenger._send_json(FakeSendFile(), {"key": "value"}) is False


def test_join_server_failure():
    """Testing _join_server returns false if join message not sent."""
    messenger = DirectMessenger(("clotho.ics.uci.edu, 2021"), "user", "pass")

    class FakeSendFile:
        def write(self, _):
            raise OSError("write failed")

        def flush(self):
            return None

    class FakeRecvFile:
        def readline(self):
            return ""

    assert messenger._join_server(FakeSendFile(), FakeRecvFile()) is False
