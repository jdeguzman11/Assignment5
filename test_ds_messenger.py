# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# test_ds_messenger.py

"""Unit tests for ds_messenger file."""

from ds_messenger import DirectMessage, DirectMessenger


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
