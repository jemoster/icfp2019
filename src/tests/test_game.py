import unittest
import os
import game
from tests.util import EXAMPLES_DIR

class TestStringMethods(unittest.TestCase):

    def test_loading(self):
        game.loader(EXAMPLES_DIR+'/example-01.desc')

if __name__ == '__main__':
    unittest.main()