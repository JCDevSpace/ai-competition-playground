#!/usr/bin/python

import unittest
import imp

xgui = imp.load_source('xgui', '../../D/')

class XGuiTestArgs(unittest.TestCase):
  '''
  no args
  too big of a number
  negative number
  not a number
  too many args
  a good one
  '''

  def test_no_args(self):
    self.assertEqual(xgui.get_size_from_args(['xgui']), "Usage:   ./xgui positive-integer")

  def test_too_many_args(self):
    self.assertEqual(xgui.get_size_from_args(['xgui', '2', '40']), "Usage:   ./xgui positive-integer")

  def test_not_a_number(self):
    self.assertEqual(xgui.get_size_from_args(['xgui', 'y']), "Usage:   ./xgui positive-integer")

  def test_negative_number(self):
    self.assertEqual(xgui.get_size_from_args(['xgui', '-8']), "Usage:   ./xgui positive-integer")

  def test_big_number(self):
    self.assertEqual(xgui.get_size_from_args(['xgui', '8000']), "Error:   Size must be between 1 and 300")

  def test_a_good_number(self):
    self.assertEqual(xgui.get_size_from_args(['xgui', '40']), 40)

if __name__ == '__main__':
  unittest.main()
