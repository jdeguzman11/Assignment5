# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# ds_messenger.py

"""Classes for sending/receiving messages from DS server."""

import socket
import time
import json

import ds_protocol


# pylint: disable=too-few-public-methods
class DirectMessage:
    """Represents a direct message."""

    def __init__(self, recipient=None, message=None, timestamp=None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    """Handles direct messaging with the DS server."""

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None

    def send(self, message: str, recipient: str) -> bool:
        """Sends a direct message."""
        sock = self._connect()
        if sock is None:
            return False

        send_file = None
        recv_file = None

        try:
            send_file = sock.makefile("w", encoding="utf-8", newline="")
            recv_file = sock.makefile("r", encoding="utf-8", newline="")

            if not self._join_server(send_file, recv_file):
                return False

            timestamp = str(time.time())

            msg = ds_protocol.create_direct_message(
                self.token,
                message,
                recipient,
                timestamp
            )

            if not self._send_json(send_file, json.loads(msg)):
                return False

            response = self._recv_response(recv_file)
            return response.type == "ok"

        except Exception:
            return False

        finally:
            try:
                if send_file is not None:
                    send_file.close()
            except Exception:
                pass

            try:
                if recv_file is not None:
                    recv_file.close()
            except Exception:
                pass

            try:
                sock.close()
            except Exception:
                pass

    def retrieve_new(self) -> list:
        """Retrieves new direct messages."""
        return self._retrieve_messages("new")

    def retrieve_all(self) -> list:
        """Retrieves all direct messages."""
        return self._retrieve_messages("all")

    def _retrieve_messages(self, request_type: str) -> list:
        """Retrieve direct messages from DS server."""
        sock = self._connect()
        if sock is None:
            return []

        send_file = None
        recv_file = None

        try:
            send_file = sock.makefile("w", encoding="utf-8", newline="")
            recv_file = sock.makefile("r", encoding="utf-8", newline="")

            if not self._join_server(send_file, recv_file):
                return []

            if request_type == "new":
                msg = ds_protocol.create_get_new(self.token)
            else:
                msg = ds_protocol.create_get_all(self.token)

            if not self._send_json(send_file, json.loads(msg)):
                return []

            response = recv_file.readline()
            messages = ds_protocol.extract_direct_messages(response.strip())

            direct_messages = []
            for msg_obj in messages:
                direct_message = DirectMessage(
                    msg_obj.from_user,
                    msg_obj.message,
                    msg_obj.timestamp
                )
                direct_messages.append(direct_message)

            return direct_messages

        except Exception:
            return []

        finally:
            try:
                if send_file is not None:
                    send_file.close()
            except Exception:
                pass

            try:
                if recv_file is not None:
                    recv_file.close()
            except Exception:
                pass

            try:
                sock.close()
            except Exception:
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

    def _send_json(self, send_file, message: dict) -> bool:
        """Send JSON message to DS server."""
        try:
            json_msg = json.dumps(message)
            send_file.write(json_msg + "\r\n")
            send_file.flush()
            return True
        except Exception:
            return False

    def _recv_response(self, recv_file):
        """Receive response from DS server."""
        try:
            line = recv_file.readline()
            if line == "":
                return ds_protocol.DataTuple(None, None)

            return ds_protocol.extract_json(line.strip())
        except Exception:
            return ds_protocol.DataTuple(None, None)

    def _join_server(self, send_file, recv_file) -> bool:
        """Join DS server and store returned token."""
        join_msg = {
            "join": {
                "username": self.username,
                "password": self.password,
                "token": ""
            }
        }

        if not self._send_json(send_file, join_msg):
            return False

        response = self._recv_response(recv_file)
        if response.type != "ok":
            return False

        if not response.token:
            return False

        self.token = response.token
        return True
