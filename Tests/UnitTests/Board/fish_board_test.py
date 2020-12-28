from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Common.fish_board import FishBoard


class FishBoardTestUniformBoard(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_bad_num_fish(self):
        self.assertFalse(self.no_preset_board.make_uniform_board(0))
        self.assertFalse(self.no_preset_board.make_uniform_board(1000))

    def test_min_num_fish(self):
        self.assertTrue(self.no_preset_board.make_uniform_board(self.min_fish))

    def test_max_num_fish(self):
        self.assertTrue(self.no_preset_board.make_uniform_board(self.max_fish))
        
    def test_preset_layout(self):
        self.assertFalse(self.preset_board.make_uniform_board(self.min_fish))
        self.assertFalse(self.preset_board.make_limited_board(self.max_fish))


class FishBoardTestLimitedBoard(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_bad_num_fish(self):
        self.assertFalse(self.no_preset_board.make_limited_board(0))
        self.assertFalse(self.no_preset_board.make_limited_board(self.rows * self.cols + 1))

    def test_small_num_fish(self):
        self.assertTrue(self.no_preset_board.make_limited_board(1))

    def test_meidum_num_fish(self):
        self.assertTrue(self.no_preset_board.make_limited_board(8))

    def test_large_num_fish(self):
        self.assertTrue(self.no_preset_board.make_limited_board(self.rows * self.cols))
    
    def test_preset_layout(self):
        self.assertFalse(self.preset_board.make_limited_board(10))
        self.assertFalse(self.preset_board.make_limited_board(5))


class FishBoardTestSetFish(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_preset_set(self):
        self.assertTrue(self.preset_board.set_fish(1, (1,1)))
        self.assertTrue(self.preset_board.set_fish(3, (2, 3)))

    def test_set_before_layout(self):
        self.assertFalse(self.no_preset_board.set_fish(1, (1,1)))
        self.assertFalse(self.no_preset_board.set_fish(3, (2,3)))

    def test_set_after_layout1(self):
        self.no_preset_board.make_uniform_board(3)
        self.assertTrue(self.no_preset_board.set_fish(2, (0,0)))
        self.assertTrue(self.no_preset_board.set_fish(5, (2,3)))

    def test_set_after_layout2(self):
        self.no_preset_board.make_limited_board(5)
        self.assertTrue(self.no_preset_board.set_fish(2, (0,0)))
        self.assertTrue(self.no_preset_board.set_fish(5, (2,3)))

    def test_bad_set(self):
        self.assertFalse(self.no_preset_board.set_fish(0, (-1,-1)))
        self.assertFalse(self.no_preset_board.set_fish(-1, (1,1)))
        self.assertFalse(self.no_preset_board.set_fish(3, (20, 10)))
        self.assertFalse(self.preset_board.set_fish(0, (-1,-1)))
        self.assertFalse(self.preset_board.set_fish(-1, (1,1)))
        self.assertFalse(self.preset_board.set_fish(3, (20, 10)))       


class FishBoardTestSetHole(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_preset_set(self):
        self.assertTrue(self.preset_board.set_hole((1,1)))
        self.assertTrue(self.preset_board.set_hole((2, 3)))

    def test_set_before_layout(self):
        self.assertFalse(self.no_preset_board.set_hole((1,1)))
        self.assertFalse(self.no_preset_board.set_hole((2,3)))

    def test_set_after_layout1(self):
        self.no_preset_board.make_uniform_board(3)
        self.assertTrue(self.no_preset_board.set_hole((0,0)))
        self.assertTrue(self.no_preset_board.set_hole((2,3)))

    def test_set_after_layout2(self):
        self.no_preset_board.make_limited_board(5)
        self.assertTrue(self.no_preset_board.set_hole((0,0)))
        self.assertTrue(self.no_preset_board.set_hole((2,3)))

    def test_bad_set(self):
        self.assertFalse(self.no_preset_board.set_hole((-1,-1)))
        self.assertFalse(self.no_preset_board.set_hole((20, 10)))
        self.assertFalse(self.preset_board.set_hole((-1,-1)))
        self.assertFalse(self.preset_board.set_hole((20, 10)))


class FishBoardTestActions(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

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
            self.assertEqual(self.preset_board.apply_action("red", bad_action), (False, 0))
            self.assertEqual(self.no_preset_board.apply_action("red", bad_action), (False, 0))

    
    def test_preset_actions(self):
        output = self.preset_board.valid_actions("red")
        
        expected_output = [
            (0,0), (0,1), (0,3),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2), (2,3)
        ]

        self.assertEqual(output, expected_output)

        self.assertTrue(self.preset_board.set_hole((2,3)))
        self.assertTrue(self.preset_board.set_hole((0,0)))

        output = self.preset_board.valid_actions("red")
        
        expected_output = [
            (0,1), (0,3),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)
        ]

        self.assertEqual(output, expected_output)

        bad_apply_results = (False, 0)

        self.assertEqual(self.preset_board.apply_action("red", (0,0)), bad_apply_results)
        self.assertEqual(self.preset_board.apply_action("red", (2,3)), bad_apply_results)

        output = self.preset_board.apply_action("red", (0,1))

        expected_output = (True, 4)

        self.assertEqual(output, expected_output)

        self.assertEqual(self.preset_board.apply_action("green", (0,1)), bad_apply_results)

        output = self.preset_board.apply_action("green", (0,3))

        expected_output = (True, 4)

        self.assertEqual(output, expected_output)

        output = self.preset_board.apply_action("green", (2,1))

        expected_output = (True, 4)

        self.assertEqual(output, expected_output)

        output = self.preset_board.apply_action("red", (2,2))

        expected_output = (True, 5)

        self.assertEqual(output, expected_output)

        output = self.preset_board.valid_actions("red")

        expected_output = [
            ((0,1),(1,0)), ((0,1), (2,0)), ((0,1), (1,1)),
            ((2,2), (1,1)), ((2,2), (1,2))
        ]

        self.assertEqual(output, expected_output)

        output = self.preset_board.valid_actions("green")

        expected_output = [
            ((0,3), (1,2)),
            ((2,1), (1,0)), ((2,1), (1,1))
        ]

        self.assertEqual(output, expected_output)

        self.assertEqual(self.preset_board.apply_action("red", ((0,3), (1,1))), bad_apply_results)
        self.assertEqual(self.preset_board.apply_action("green", ((0,3), (1,1))), bad_apply_results)

        output = self.preset_board.apply_action("red", ((0,1),(1,0)))

        expected_output = (True, 2)

        self.assertEqual(output, expected_output)

        output = self.preset_board.apply_action("green", ((0,3),(1,2)))

        expected_output = (True, 3)

        self.assertEqual(output, expected_output)


    def test_no_preset_actions(self):
        self.assertFalse(self.no_preset_board.valid_actions("red"))

        self.no_preset_board.make_uniform_board(2)

        output = self.no_preset_board.valid_actions("red")

        expected_output = [
            (0,0),(0,1),(0,2),(0,3),
            (1,0),(1,1),(1,2),(1,3),
            (2,0),(2,1),(2,2),(2,3),
            (3,0),(3,1),(3,2),(3,3)
        ]

        self.assertEqual(output, expected_output)

        self.assertTrue(self.no_preset_board.set_hole((0,3)))
        self.assertTrue(self.no_preset_board.set_hole((1,3)))
        self.assertTrue(self.no_preset_board.set_hole((2,3)))
        self.assertTrue(self.no_preset_board.set_hole((3,3)))
        self.assertTrue(self.no_preset_board.set_hole((3,1)))
        self.assertTrue(self.no_preset_board.set_hole((3,2)))
        self.assertTrue(self.no_preset_board.set_hole((3,0)))

        output = self.no_preset_board.valid_actions("red")

        expected_output = [
            (0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2)
        ]

        self.assertEqual(output, expected_output)

        bad_apply_results = (False, 0)

        expected_output = (True, 2)

        self.assertEqual(self.no_preset_board.apply_action("red", (0,3)), bad_apply_results)
        self.assertEqual(self.no_preset_board.apply_action("red", (3,3)), bad_apply_results)

        output = self.no_preset_board.apply_action("red", (0,0))

        self.assertEqual(output, expected_output)

        self.assertEqual(self.no_preset_board.apply_action("green", (0,0)), bad_apply_results)

        output = self.no_preset_board.apply_action("green", (0,1))

        self.assertEqual(output, expected_output)

        output = self.no_preset_board.apply_action("green", (2,1))

        self.assertEqual(output, expected_output)

        output = self.no_preset_board.apply_action("red", (2,2))

        self.assertEqual(output, expected_output)

        output = self.no_preset_board.valid_actions("red")

        expected_output = [
            ((0, 0), (2, 0)), ((0, 0), (1, 0)),
            ((2, 2), (0, 2)), ((2, 2), (1, 1)), ((2, 2), (1, 2))
        ]

        self.assertEqual(output, expected_output)

        output = self.no_preset_board.valid_actions("green")

        expected_output = [
            ((0,1),(1,0)),((0,1),(2,0)),((0,1),(1,1)),
            ((2,1),(1,0)),((2,1),(1,1)),((2,1),(0,2))
        ]

        self.assertEqual(output, expected_output)

        expected_output = (True, 2)

        self.assertEqual(self.no_preset_board.apply_action("red", ((0,0), (1,1))), bad_apply_results)
        self.assertEqual(self.no_preset_board.apply_action("green", ((0,3), (1,1))), bad_apply_results)

        output = self.no_preset_board.apply_action("red", ((0,0),(1,0)))

        self.assertEqual(output, expected_output)

        output = self.no_preset_board.apply_action("green", ((2,1),(0,2)))

        self.assertEqual(output, expected_output)


class FishBoardTestSerialize(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_serialize_no_layout(self):
        output = self.no_preset_board.serialize()
        
        expected_output = {
            "layout": [],
            "avatars": {}
        }

        self.assertEqual(output, expected_output)

    def test_serlized_made_layout(self):
        self.no_preset_board.make_uniform_board(2)
        
        output = self.no_preset_board.serialize()
        
        expected_output = {
            "layout": [[2,2,2,2], [2,2,2,2], [2,2,2,2], [2,2,2,2]],
            "avatars": {}
        }

        self.assertEqual(output, expected_output)

    def test_serilize_preset_layout(self):
        output = self.preset_board.serialize()
        
        expected_output = {
            "layout": [[1,4,0,4], [2,2,3,0], [2,4,5,5]],
            "avatars": {}
        }

        self.assertEqual(output, expected_output)

    def test_serilized_with_avatars(self):
        self.preset_board.apply_action("red", (0,0))
        self.preset_board.apply_action("green", (1,1))
        self.preset_board.apply_action("green", (2,3))
        self.preset_board.apply_action("blue", (3,3))

        output = self.preset_board.serialize()
        
        expected_output = {
            "layout": [[1,4,0,4], [2,2,3,0], [2,4,5,5]],
            "avatars": {
                "green": [(1,1), (2,3)],
                "red": [(0,0)],
            }
        }

        self.assertEqual(output, expected_output)



if __name__ == "__main__":
    unittest.main()