from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Common.marble_board import MarbleBoard

class MarbleBoardTestInitilization(unittest.TestCase):
    def test_proper_layout(self):
        board = MarbleBoard()
        
        output = board.serialize()

        layout = output["layout"]

        expected_layout = [
            [2,2,1,1,1,2,2],
            [2,2,1,1,1,2,2],
            [1,1,1,1,1,1,1],
            [1,1,1,0,1,1,1],
            [1,1,1,1,1,1,1],
            [2,2,1,1,1,2,2],
            [2,2,1,1,1,2,2]
        ]

        self.assertEqual(layout, expected_layout)


class MarbleBoardTestActions(unittest.TestCase):
    def setUp(self):
        self.test_board = MarbleBoard()
    
    def test_apply_bad_actions(self):
        bad_actions = [
            1,
            True,
            "True",
            (-1,5),
            ((1,1), False),
            ("False", (1,1)),
            (4,4),
            ((1,1), (4,4)),
            ((4,4), (1,1))
        ]

        for bad_action in bad_actions:
            self.assertEqual(self.test_board.apply_action("red", bad_action), (False, 0))

    def test_valid_actions(self):
        output = self.test_board.valid_actions("red")

        expected_output = [
            ((3, 5), (3, 3)),
            ((3, 1), (3, 3)),
            ((5, 3), (3, 3)),
            ((1, 3), (3, 3))
        ]

        self.assertEqual(output, expected_output)

    def test_apply_action(self):
        action = ((1,3), (3,3))

        self.assertEqual(self.test_board.apply_action("r", action), (True, 1))

        layout = self.test_board.serialize()["layout"]

        expected_layout = [
            [2,2,1,1,1,2,2],
            [2,2,1,0,1,2,2],
            [1,1,1,0,1,1,1],
            [1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],
            [2,2,1,1,1,2,2],
            [2,2,1,1,1,2,2]
        ]

        self.assertEqual(layout, expected_layout)

    def test_apply_multiple(self):
        actions = [
            ((1,3), (3,3)),
            ((4,3), (2,3)),
            ((3,1), (3,3)),
            ((4,5), (4,3))
        ]

        expected_actions = [
            [
                ((2, 5), (2, 3)), 
                ((2, 1), (2, 3)), 
                ((4, 3), (2, 3))
            ],
            [
                ((3, 5), (3, 3)), 
                ((3, 1), (3, 3)), 
                ((4, 5), (4, 3)), 
                ((4, 1), (4, 3)), 
                ((6, 3), (4, 3))
            ],
            [
                ((3, 3), (1, 3)),
                ((3, 4), (3, 2)), 
                ((5, 2), (3, 2)), 
                ((1, 2), (3, 2)), 
                ((4, 5), (4, 3)), 
                ((4, 1), (4, 3)), 
                ((6, 3), (4, 3)), 
                ((2, 3), (4, 3))
            ],
            [
                ((3, 3), (1, 3)), 
                ((3, 4), (3, 2)), 
                ((5, 2), (3, 2)), 
                ((1, 2), (3, 2)), 
                ((4, 2), (4, 4)), 
                ((6, 4), (4, 4)), 
                ((2, 4), (4, 4)), 
                ((2, 5), (4, 5))
            ]
        ]

        expected_layout = [
            [
                [2,2,1,1,1,2,2],
                [2,2,1,0,1,2,2],
                [1,1,1,0,1,1,1],
                [1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1],
                [2,2,1,1,1,2,2],
                [2,2,1,1,1,2,2]
            ],
            [
                [2,2,1,1,1,2,2],
                [2,2,1,0,1,2,2],
                [1,1,1,1,1,1,1],
                [1,1,1,0,1,1,1],
                [1,1,1,0,1,1,1],
                [2,2,1,1,1,2,2],
                [2,2,1,1,1,2,2]
            ],
            [
                [2,2,1,1,1,2,2],
                [2,2,1,0,1,2,2],
                [1,1,1,1,1,1,1],
                [1,0,0,1,1,1,1],
                [1,1,1,0,1,1,1],
                [2,2,1,1,1,2,2],
                [2,2,1,1,1,2,2]
            ],
            [
                [2,2,1,1,1,2,2],
                [2,2,1,0,1,2,2],
                [1,1,1,1,1,1,1],
                [1,0,0,1,1,1,1],
                [1,1,1,1,0,0,1],
                [2,2,1,1,1,2,2],
                [2,2,1,1,1,2,2]
            ]
        ]

        for i, action in enumerate(actions):
            self.assertEqual(self.test_board.apply_action("r", action), (True, 1))

            layout = self.test_board.serialize()["layout"]
            self.assertEqual(layout, expected_layout[i])

            output = self.test_board.valid_actions("r")
            self.assertEqual(output, expected_actions[i])


class MarbleBoardGameOver(unittest.TestCase):
    def setUp(self):
        self.test_board = MarbleBoard()
    
    def test_add_test_reminder(self):
        self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()