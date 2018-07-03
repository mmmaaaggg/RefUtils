import unittest
from math import ceil, floor


class MathTest(unittest.TestCase):

    def testInt(self):
        aaa = 2.5
        self.assertEqual(int(aaa), 2)

    def testRound(self):
        aaa = 2.5
        self.assertEqual(round(aaa), 3)

    def testCeil(self):
        aaa = 2.1
        self.assertEqual(ceil(aaa), 3)
        aaa = 2.9
        self.assertEqual(floor(aaa), 2)

    def testMean(self):
        aaa = [1, 2, 3]
        self.assertEqual(sum(aaa) / len(aaa), 2)
