from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from asyncio import run

from Game.Remote.signup_server import SignUpServer


from time import sleep

class TestSignupServer(unittest.TestCase):
    def setUp(self):
        self.test_server = SignUpServer()

    def test_start(self):
        run(self.test_server.start())


if __name__ == "__main__":
    unittest.main()