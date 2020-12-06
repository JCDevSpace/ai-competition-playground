import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

from Fish.Common.state import GameState
from Fish.Common.board import Board
from Fish.Remote.messages import Messages
from Fish.Remote.client import Client

import unittest
import json

from Fish.Remote.remote_player import RemotePlayer

class TestRemotePlayer(unittest.TestCase):
    def test_color_assignment(self):
        mock_connection = MockConnection(json.dumps('void'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        processed_message = remote_player.color_assignment_update('red')

        expected_sent_message = Messages.encode(Messages.PLAYING_AS, ['red'])

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertTrue(processed_message)

    def test_initial_state_update(self):
        mock_connection = MockConnection(json.dumps('void'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        state = GameState(b, [player1, player2])

        processed_message = remote_player.inital_state_update(state.get_game_state())

        expected_sent_message = Messages.encode(Messages.PLAYING_WITH, [state.get_game_state()[1]])

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertTrue(processed_message)

    def test_get_placement(self):
        mock_connection = MockConnection(json.dumps([0, 0]))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        state = GameState(b, [player1, player2])
        remote_player.state = state
        remote_player.color = 'red'

        processed_message = remote_player.get_placement()

        expected_sent_message = Messages.encode(Messages.SETUP, [Messages.convert_state(state.get_game_state())])
        expected_processed_message = ('red', (0, 0))

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertEqual(expected_processed_message, processed_message)

    def test_get_move(self):
        mock_connection = MockConnection(json.dumps([[0, 0], [0, 1]]))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        state = GameState(b, [player1, player2])
        remote_player.state = state
        remote_player.color = 'red'
        remote_player.actions = [('red', (1, 1), (1, 2))]

        expected_sent_message = Messages.encode(Messages.TAKE_TURN, [Messages.convert_state(state.get_game_state()),
                                                              Messages.convert_actions(remote_player.actions)])
        expected_processed_message = ('red', (0, 0), (0, 1))

        processed_message = remote_player.get_move()

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertEqual(expected_processed_message, processed_message)
        self.assertEqual([], remote_player.actions)

    def test_get_move_no_valid_move(self):
        mock_connection = MockConnection(json.dumps(False))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        state = GameState(b, [player1, player2])
        actions = [('red', (1, 1), (1, 2))]
        remote_player.state = state
        remote_player.color = 'red'
        remote_player.actions = actions

        expected_sent_message = Messages.encode(Messages.TAKE_TURN, [Messages.convert_state(state.get_game_state()),
                                                              Messages.convert_actions(actions)])
        expected_processed_message = ('red', False, False)

        processed_message = remote_player.get_move()

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertEqual(expected_processed_message, processed_message)

    def test_tournamnent_start_update(self):
        mock_connection = MockConnection(json.dumps('void'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        expected_sent_message = Messages.encode(Messages.START, [True])

        processed_message = remote_player.tournamnent_start_update()

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertTrue(processed_message)

    def test_tournamnent_result_update(self):
        mock_connection = MockConnection(json.dumps('void'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        expected_sent_message = Messages.encode(Messages.END, [False])

        processed_message = remote_player.tournamnent_result_update(False)

        self.assertEqual(expected_sent_message, mock_connection.message)
        self.assertTrue(processed_message)

    def test_process_response_ack(self):
        mock_connection = MockConnection(json.dumps('void'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        processed_message = remote_player.tournamnent_result_update(False)

        self.assertTrue(processed_message)

    def test_process_response_position(self):
        mock_connection = MockConnection(json.dumps([1, 3]))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)
        remote_player.color = 'red'

        processed_message = remote_player.tournamnent_result_update(False)

        self.assertEqual(('red', (1, 3)), processed_message)

    def test_process_response_action(self):
        mock_connection = MockConnection(json.dumps([[1, 3], [2, 3]]))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)
        remote_player.color = 'red'

        processed_message = remote_player.tournamnent_result_update(False)

        self.assertEqual(('red', (1, 3), (2, 3)), processed_message)

    def test_process_response_action_false(self):
        mock_connection = MockConnection(json.dumps(False))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)
        remote_player.color = 'red'

        processed_message = remote_player.tournamnent_result_update(False)

        self.assertEqual(('red', False, False), processed_message)

    def test_process_response_bad(self):
        mock_connection = MockConnection(json.dumps('this is an invalid response'))
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)
        remote_player.color = 'red'

        processed_message = remote_player.tournamnent_result_update(False)

        self.assertFalse(processed_message)

    def test_placement_update(self):
        mock_connection = MockConnection()
        remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        state_before = GameState(b, [player1, player2])
        remote_player.state = state_before.deepcopy()
        remote_player.color = 'red'

        remote_player.placement_update(('red', (0, 0)))
        self.assertEqual(state_before.get_game_state()[2], {'brown': [], 'red': []})
        self.assertEqual(remote_player.state.get_game_state()[2], {'brown': [], 'red': [(0, 0)]})

    # TODO: why invalid move?
    # def test_movement_update(self):
    #     mock_connection = MockConnection(None)
    #     remote_player = RemotePlayer('name', 0, mock_connection, 5, 4096)

    #     b = Board(3, 3, [[1, 2, 1], [1, 2, 5], [1, 1, 4]])
    #     player1 = 'red'
    #     player2 = 'brown'
    #     state_before = GameState(b, [player1, player2])
    #     remote_player.state = state_before.deepcopy()
    #     remote_player.color = 'red'
    #     remote_player.actions = []

    #     remote_player.placement_update(('red', (0, 0)))
    #     remote_player.placement_update(('brown', (2, 2)))
    #     remote_player.movement_update(('red', (0, 0), (0, 1)))

    #     self.assertEqual(state_before.get_game_state()[2], {'brown': [], 'red': []})
    #     self.assertEqual(remote_player.state.get_game_state()[2], {'brown': [], 'red': [(0, 1)]})


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
