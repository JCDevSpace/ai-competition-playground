#!/usr/bin/python3
#
#Tests for the xyes program
import unittest
import imp

xyes = imp.load_source('xyes', '../../B/xyes')


'''
Test Cases:
	no args
	contains -limit no message args
	contains -limit yes message args
	doesnt contain -limit message args


'''
class XYesTestLimit(unittest.TestCase):

	def test_no_args(self):
		self.assertEqual(xyes.get_limit(['xyes']), -1)

	def test_limit(self):
		self.assertEqual(xyes.get_limit(['xyes', '-limit']), 20)

	def test_args_no_limit(self):
		self.assertEqual(xyes.get_limit(['xyes', 'a', 'b', 'c']), -1)

	def test_limit_with_args(self):
		self.assertEqual(xyes.get_limit(['xyes', '-limit', 'x']), 20)
	


class XYesTestMessage(unittest.TestCase):

	def test_no_args(self):
		self.assertEqual(xyes.get_message(['xyes']), 'hello world')

	def test_limit(self):
		self.assertEqual(xyes.get_message(['xyes', '-limit']), 'hello world')

	def test_args_no_limit(self):
		self.assertEqual(xyes.get_message(['xyes', 'a', 'b', 'c']), 'a b c')

	def test_limit_with_args(self):
		self.assertEqual(xyes.get_message(['xyes', '-limit', 'x']), 'x')
	


if __name__ == '__main__':
	unittest.main()

