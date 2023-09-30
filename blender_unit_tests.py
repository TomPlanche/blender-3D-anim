"""
This file is used to run unit tests for the blender_test.py file.
"""

import unittest
import numpy as np
from blender_test import Vector


class MyTestCase(unittest.TestCase):
    def test_vector_class_add(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)

        self.assertEqual(v1 + v2, Vector(5, 7, 9))

    def test_vector_class_del(self):
        v1 = Vector(5, 7, 9)
        v2 = Vector(4, 5, 6)

        self.assertEqual(v1 - v2, Vector(1, 2, 3))

    def test_vector_class_mul(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)

        self.assertEqual(v1 * v2, Vector(4, 10, 18))

    def test_vector_class_div(self):
        v1 = Vector(4, 10, 18)
        v2 = Vector(4, 5, 6)

        self.assertEqual(v1 / v2, Vector(1, 2, 3))

    def test_vector_class_eq(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 3)

        self.assertEqual(v1, v2)


if __name__ == '__main__':
    unittest.main()
