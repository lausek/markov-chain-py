import pytest

from .deps import *

from markov_chain_py.spacy_chain import *

class TestSpacy(Test):
    def test_pos_lookback_one(self, example_data):
        gen = SpacyPosMarkovChain('de_core_news_sm', lookback=1)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_pos_lookback_two(self, example_data):
        gen = SpacyPosMarkovChain('de_core_news_sm', lookback=2)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_pos_lookback_three(self, example_data):
        gen = SpacyPosMarkovChain('de_core_news_sm', lookback=3)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_tag_lookback_one(self, example_data):
        gen = SpacyTagMarkovChain('de_core_news_sm', lookback=1)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_tag_lookback_two(self, example_data):
        gen = SpacyTagMarkovChain('de_core_news_sm', lookback=2)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))

    def test_tag_lookback_three(self, example_data):
        gen = SpacyTagMarkovChain('de_core_news_sm', lookback=3)
        gen.add_string(example_data)

        self.assertTrue(gen.generate(n=20))
        self.assertTrue(gen.generate_text(s=4))
