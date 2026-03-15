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
