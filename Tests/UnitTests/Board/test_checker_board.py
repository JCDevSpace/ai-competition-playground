from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Common.checker_board import CheckerBoard
from Game.Common.action import Action

class CheckerBoardTestInitialization(unittest.TestCase):
    def setUp(self):
        self.test_board = CheckerBoard()

    def test_proper_default_board(self):
        output = self.test_board.serialize()

        layout = output["layout"]
        avatars = output["avatars"]

        expected_layout = [
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]

        ]

        expected_avatars = {
            "white": [
                (0, 1), (0, 3), (0, 5), (0, 7), 
                (1, 0), (1, 2), (1, 4), (1, 6), 
                (2, 1), (2, 3), (2, 5), (2, 7)
            ],
            "red": [
                (5, 0), (5, 2), (5, 4), (5, 6), 
                (6, 1), (6, 3), (6, 5), (6, 7), 
                (7, 0), (7, 2), (7, 4), (7, 6)
            ]
        }
        self.assertEqual(layout, expected_layout)
        self.assertEqual(avatars, expected_avatars)


class CheckerBoardTestActions(unittest.TestCase):
    def setUp(self):
        self.test_board = CheckerBoard()

    def test_get_default_valid_actions(self):
        actions = self.test_board.valid_actions("white")

        expected_actions = [
            ((2, 1), (3, 0)), ((2, 1), (3, 2)), 
            ((2, 3), (3, 2)), ((2, 3), (3, 4)), 
            ((2, 5), (3, 4)), ((2, 5), (3, 6)), 
            ((2, 7), (3, 6))
        ]

        self.assertEqual(actions, expected_actions)

        actions = self.test_board.valid_actions("red")

        expected_actions = [
            ((5, 0), (4, 1)), 
            ((5, 2), (4, 1)), ((5, 2), (4, 3)), 
            ((5, 4), (4, 3)), ((5, 4), (4, 5)), 
            ((5, 6), (4, 5)), ((5, 6), (4, 7))
        ]
        self.assertEqual(actions, expected_actions)

    def test_apply_bad_action(self):
        bad_actions = [
            1,
            True,
            "True",
            (-1,5),
            ((1,1), False),
            ("False", (1,1)),
            (4,4),
            ((5,0), (4,4)),
            ((4,4), (4,5)),
            ((9,1), (1,9))
        ]
        for bad_action in bad_actions:
            self.assertEqual(self.test_board.apply_action("red", bad_action), (False, 0))

    def test_apply_actions(self):
        expected_actions = [
            [
                ((2, 1), (3, 0)), ((2, 1), (3, 2)), 
                ((2, 3), (3, 2)), ((2, 3), (3, 4)), 
                ((2, 5), (3, 4)), ((2, 5), (3, 6)), 
                ((2, 7), (3, 6))
            ],
            [
                ((5, 0), (4, 1)), 
                ((5, 2), (4, 1)), ((5, 2), (4, 3)), 
                ((5, 4), (4, 3)), ((5, 4), (4, 5)), 
                ((5, 6), (4, 5)), ((5, 6), (4, 7))
            ],
            [
                ((1, 6), (2, 7)),
                ((2, 1), (3, 0)), ((2, 1), (3, 2)), 
                ((2, 3), (3, 2)), ((2, 3), (3, 4)), 
                ((2, 5), (3, 4)),
                ((3, 6), (4, 5)), ((3, 6), (4, 7))
            ],
            [
                ((4, 1), (3, 0)), ((4, 1), (3, 2)),
                ((5, 2), (4, 3)), 
                ((5, 4), (4, 3)), ((5, 4), (4, 5)), 
                ((5, 6), (4, 5)),
                ((6, 1), (5, 0)),
            ],
            [
                ((2, 1), (4, 3)), 
                ((2, 3), (4, 1)), 
            ],
            [
                ((5, 2), (3, 4)), 
                ((5, 4), (3, 2)), 
            ]
        ]

        expected_layouts = [
            [
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,0],
                [0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]
            ],
            [
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,0],
                [0,0,0,0,0,0,1,0],
                [0,1,0,0,0,0,0,0],
                [0,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]
            ],
            [
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,0],
                [0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,1],
                [0,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]
            ],
            [
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,0],
                [0,0,1,0,0,0,0,0],
                [0,0,0,0,0,0,0,1],
                [0,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]
            ],
            [
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,0,0,1,0,1,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,1,0,0,0,1],
                [0,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]
            ],
            [
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,0,0,1,0,1,0,0],
                [0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,1],
                [0,0,0,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]
            ],
        ]

        expected_avatars = [
            {
                "white": [
                    (0, 1), (0, 3), (0, 5), (0, 7), 
                    (1, 0), (1, 2), (1, 4), (1, 6), 
                    (2, 1), (2, 3), (2, 5), (3, 6)
                ],
                "red": [
                    (5, 0), (5, 2), (5, 4), (5, 6), 
                    (6, 1), (6, 3), (6, 5), (6, 7), 
                    (7, 0), (7, 2), (7, 4), (7, 6)
                ]
            },
            {
                "white": [
                    (0, 1), (0, 3), (0, 5), (0, 7), 
                    (1, 0), (1, 2), (1, 4), (1, 6), 
                    (2, 1), (2, 3), (2, 5), (3, 6)
                ],
                "red": [
                    (4, 1), (5, 2), (5, 4), (5, 6), 
                    (6, 1), (6, 3), (6, 5), (6, 7), 
                    (7, 0), (7, 2), (7, 4), (7, 6)
                ]
            },
            {
                "white": [
                    (0, 1), (0, 3), (0, 5), (0, 7), 
                    (1, 0), (1, 2), (1, 4), (1, 6), 
                    (2, 1), (2, 3), (2, 5), (4, 7)
                ],
                "red": [
                    (4, 1), (5, 2), (5, 4), (5, 6), 
                    (6, 1), (6, 3), (6, 5), (6, 7), 
                    (7, 0), (7, 2), (7, 4), (7, 6)
                ]
            },
            {
                "white": [
                    (0, 1), (0, 3), (0, 5), (0, 7), 
                    (1, 0), (1, 2), (1, 4), (1, 6), 
                    (2, 1), (2, 3), (2, 5), (4, 7)
                ],
                "red": [
                    (3, 2), (5, 2), (5, 4), (5, 6), 
                    (6, 1), (6, 3), (6, 5), (6, 7), 
                    (7, 0), (7, 2), (7, 4), (7, 6)
                ]
            },
            {
                "white": [
                    (0, 1), (0, 3), (0, 5), (0, 7), 
                    (1, 0), (1, 2), (1, 4), (1, 6), 
                    (4, 3), (2, 3), (2, 5), (4, 7)
                ],
                "red": [
                    (5, 2), (5, 4), (5, 6), 
                    (6, 1), (6, 3), (6, 5), (6, 7), 
                    (7, 0), (7, 2), (7, 4), (7, 6)
                ]
            },
            {
                "white": [
                    (0, 1), (0, 3), (0, 5), (0, 7), 
                    (1, 0), (1, 2), (1, 4), (1, 6), 
                    (2, 3), (2, 5), (4, 7)
                ],
                "red": [
                    (3, 4), (5, 4), (5, 6), 
                    (6, 1), (6, 3), (6, 5), (6, 7), 
                    (7, 0), (7, 2), (7, 4), (7, 6)
                ]
            },
            
        ]

        good_apply = (True, 1)

        actions = [
            ["white", ((2,7), (3,6))],
            ["red", ((5,0), (4,1))],
            ["white", ((3,6), (4,7))],
            ["red", ((4,1), (3,2))],
            ["white", ((2,1), (4,3))],
            ["red", ((5,2), (3,4))],
        ]

        for i, (player, action) in enumerate(actions):
            output_actions = self.test_board.valid_actions(player)

            self.assertEqual(output_actions, expected_actions[i])

            self.assertEqual(self.test_board.apply_action(player, action), good_apply)

            output = self.test_board.serialize()

            layout = output["layout"]
            avatars = output["avatars"]

            self.assertEqual(layout, expected_layouts[i])
            self.assertEqual(avatars, expected_avatars[i])

    def test_regular_king_moves(self):
        custom_avatars = {
            "white": [
                (1,4), (1,6),
                (3,4), (3,6)
            ],
            "red": [
                (2,5)
            ]
        }

        custom_layout = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,1,0],
            [0,0,0,0,0,2,0,0],
            [0,0,0,0,1,0,1,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        expected_layouts = [
            [
                [0,0,0,2,0,0,0,0],
                [0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,1,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ],
            [
                [0,0,0,0,0,0,0,2],
                [0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,1,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ],
            [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,1,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,0],
                [0,0,0,2,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ],
            [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,1,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,2],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]
        ]

        self.test_board.set_custom_board(custom_avatars, custom_layout)

        output_actions = self.test_board.valid_actions("red")
        
        expected_actions = [
            ((2, 5), (0, 3)), 
            ((2, 5), (0, 7)), 
            ((2, 5), (4, 3)), 
            ((2, 5), (4, 7))
        ]

        self.assertEqual(output_actions, expected_actions)

        actions = [
            ((2, 5), (0, 3)), 
            ((2, 5), (0, 7)), 
            ((2, 5), (4, 3)), 
            ((2, 5), (4, 7))
        ]

        for i, action in enumerate(actions):
            self.test_board.set_custom_board(custom_avatars, custom_layout)

            self.assertEqual(self.test_board.apply_action("red", action), (True, 1))

            output = self.test_board.serialize()
            
            layout = output["layout"]

            self.assertEqual(layout, expected_layouts[i])

    def test_edge_king_moves(self):
        custom_avatars = {
            "white": [
                (1,2), (1,4),
                (7,4)
            ],
            "red": [
                (0,3),
                (6,3), (6,5)
            ]
        }

        custom_layout = [
            [0,0,0,2,0,0,0,0],
            [0,0,1,0,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,0,1,0,0],
            [0,0,0,0,2,0,0,0]
        ]

        expected_actions = [
            [((0,3), (2,1)), ((0,3), (2,5))],
            [((7,4), (5,2)), ((7,4), (5,6))],
        ]

        players = ["red", "white"]

        for i, player in enumerate(players):

            self.test_board.set_custom_board(custom_avatars, custom_layout)

            output_actions = self.test_board.valid_actions(player)

            self.assertEqual(output_actions, expected_actions[i])


        expected_layouts = [
            [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0],
                [0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,1,0,1,0,0],
                [0,0,0,0,2,0,0,0]
            ],
            [
                [0,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0],
                [0,0,0,0,0,2,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,1,0,1,0,0],
                [0,0,0,0,2,0,0,0]
            ],
            [
                [0,0,0,2,0,0,0,0],
                [0,0,1,0,1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,2,0,0,0,0,0],
                [0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,0]
            ],
            [
                [0,0,0,2,0,0,0,0],
                [0,0,1,0,1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,2,0],
                [0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,0,0]
            ]
        ]

        actions = [
            ["red", ((0,3), (2,1))],
            ["red", ((0,3), (2,5))],
            ["white", ((7,4), (5,2))], 
            ["white", ((7,4), (5,6))]
        ]

        for i, (player, action) in enumerate(actions):
            self.test_board.set_custom_board(custom_avatars, custom_layout)

            self.assertEqual(self.test_board.apply_action(player, action), (True, 1))

            output = self.test_board.serialize()
            
            layout = output["layout"]

            self.assertEqual(layout, expected_layouts[i])


    def test_turn_king(self):
        custom_avatars = {
            "white": [
                (1,2), (1,4),
                (5,6), (6,7)
            ],
            "red": [
                (1,0), (2,1),
                (6,3), (6,5)
            ]
        }

        custom_layout = [
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,0,0],
            [0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,0]
        ]

        red_expected_actions = [
            [((2, 1), (0, 3)), ((6, 5), (4, 7))],
            [((0, 3), (2, 5))],
            [
                ((1, 0), (0, 1)),
                ((2, 5), (1, 4)),
                ((2, 5), (1, 6)),
                ((2, 5), (3, 4)),
                ((2, 5), (3, 6))
            ]
        ]

        white_expected_actions = [
            [((1, 2), (3, 0)), ((5, 6), (7, 4))],
            [((7, 4), (5, 2))],
            [
                ((5, 2), (4, 1)),
                ((5, 2), (4, 3)),
                ((5, 2), (6, 1)),
                ((5, 2), (6, 3)),
                ((6, 7), (7, 6))
            ]
        ]

        self.test_board.set_custom_board(custom_avatars, custom_layout)

        actions = [
            [((2,1), (0,3)), ((5,6), (7,4))],
            [((0,3), (2,5)), ((7,4), (5,2))],
            [((1,0), (0,1)), ((6,7), (7,6))]
        ]

        for i, (red_action, white_action) in enumerate(actions):
            ouput_actions = self.test_board.valid_actions("red")
            
            self.assertEqual(ouput_actions, red_expected_actions[i])

            ouput_actions = self.test_board.valid_actions("white")
            
            self.assertEqual(ouput_actions, white_expected_actions[i])

            self.assertEqual(self.test_board.apply_action("red", red_action), (True, 1))

            self.assertEqual(self.test_board.apply_action("white", white_action), (True, 1))


        expected_final_layout = [
            [0,2,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,2,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,2,0]
        ]

        expected_final_avatars = {
            "white": [
                (5,2), (7,6)
            ],
            "red": [
                (0,1), (2,5)
            ]
        }

        output = self.test_board.serialize()
            
        layout = output["layout"]
        avatars = output["avatars"]

        self.assertEqual(layout, expected_final_layout)
        self.assertEqual(avatars, expected_final_avatars)


if __name__ == "__main__":
    unittest.main()