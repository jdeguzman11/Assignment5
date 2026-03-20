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
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    assert messenger.dsuserver == ("clotho.ics.uci.edu", 2021)
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


def test_send_json_success():
    """Testing _send_json returns true."""
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    class FakeSendFile:
        def write(self, _):
            return None

        def flush(self):
            return None

    class FakeRecvFile:
        def readline(self):
            return '{"response":{"type":"ok","token":"hello"}}\n'

    assert messenger._join_server(FakeSendFile(), FakeRecvFile()) is True
    assert messenger.token == "hello"


def test_join_server_success():
    """Testing _join_server returns true and has token."""
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    class FakeSendFile:
        def write(self, _):
            return None

        def flush(self):
            return None

    class FakeRecvFile:
        def readline(self):
            return '{"response":{"type":"ok","token":"hello"}}\n'

    assert messenger._join_server(FakeSendFile(), FakeRecvFile()) is True
    assert messenger.token == "hello"


def test_join_server_repsonse_bad():
    """Testing _join_server returns false on bad response."""
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    class FakeSendFile:
        def write(self, _):
            return None

        def flush(self):
            return None

    class FakeRecvFile:
        def readline(self):
            return '{"response":{"type":"error"}}\n'

    assert messenger._join_server(FakeSendFile(), FakeRecvFile()) is False


def test_recv_response_valid():
    """Test _recv_response with valid server response."""
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    class FakeRecvFile:
        def readline(self):
            return '{"response":{"type":"ok","token":"hello"}}\n'

    result = messenger._recv_response(FakeRecvFile())

    assert result.type == "ok"
    assert result.token == "hello"


def test_retrieve_messages_exception():
    """Test _retrieve_messages returns empty list when exception."""
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    class FakeSocket:
        def makefile(self, *_args, **_kwargs):
            raise OSError("fail")

        def close(self):
            return None

    def fake_connect():
        return FakeSocket()

    messenger._connect = fake_connect

    assert messenger._retrieve_messages("new") == []


def test_send_exception():
    """Testing senf returns false."""
    messenger = DirectMessenger(("clotho.ics.uci.edu", 2021), "user", "pass")

    class FakeSocket:
        def makefile(self, *_args, **_kwargs):
            raise OSError("fail")

        def close(self):
            return None

    def fake_connect():
        return FakeSocket()

    messenger._connect = fake_connect

    assert messenger.send("hello", "jdawg") is False
