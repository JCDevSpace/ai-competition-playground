import unittest
import imp

xyes = imp.load_source('xyes', '../B/xyes')

print xyes.get_limit([])

