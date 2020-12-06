import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

from Fish.Remote.remote_player import RemotePlayer
import unittest

class TestColorAssignment(unittest.TestCase):
    def test_one(self):
    mock_connection = MockConnection('myMessage')
    remote_player = RemotePlayer('name', 0, self.mock_connection, 5, 4096)

    self.assertEqual('expected', remote_player.color_assignment_update('red'))

class MockConnection:
    def __init__(self, resp_msg=None):
       self.resp_msg = resp_msg
       self.message = None

    def sendall(self, message):
        self.message = message

    def recv(self, buff_size):
        return self.resp_msg

    def setimeout():
        pass


if __name__ == '__main__':
    unittest.main()