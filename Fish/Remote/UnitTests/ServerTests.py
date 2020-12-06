import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

import unittest

class TestServer(unittest.TestCase):
    def test_minimum_signup(self):
        mock_connection = MockConnection(json.dumps('void'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        processed_message = remote_player.color_assignment_update('red')

        expected_sent_message = Messages.encode(Messages.PLAYING_AS, ['red'])

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertTrue(processed_message)


class MockConnection:
    def __init__(self, resp_msg=None):
       self.resp_msg = resp_msg
       self.message = None

    def sendall(self, message):
        self.message = message

    def recv(self, buff_size):
        return self.resp_msg

    def settimeout(self, timeout):
        pass


if __name__ == '__main__':
    unittest.main()
