import pytest

from .deps import *

from markov_chain_py.ngram_chain import *

class TestChain(Test):
    def test_lookback_one(self, example_data):
        gen = NGramMarkovChain(lookback=1)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_lookback_two(self, example_data):
        gen = NGramMarkovChain(lookback=2)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_lookback_three(self, example_data):
        gen = NGramMarkovChain(lookback=3)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_keep_newlines(self):
        gen = NGramMarkovChain(lookback=1)
        gen.add_string("a b c\nd e f")

        with pytest.raises(KeyError):
            self.assertTrue(gen.table.get('\n'))

        gen = NGramMarkovChain(lookback=1)
        gen.enable_keep_newlines()
        gen.add_string("a b c\nd e f")

        self.assertTrue(gen.table.get('\n'))
