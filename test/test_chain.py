import pytest

from .deps import *

class TestChain(Test):
    def test_lookback_one(self, example_data):
        gen = MarkovChain(lookback=1)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_lookback_two(self, example_data):
        gen = MarkovChain(lookback=2)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_lookback_three(self, example_data):
        gen = MarkovChain(lookback=3)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))
