from os.path import abspath, dirname, join

import os
import pytest
import sys

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from markov_chain_py import *

class Test:
    def assertTrue(self, expr):
        assert expr

@pytest.fixture()
def example_data():
    from pathlib import Path

    path = Path(sys.path[0]) / 'examples' / 'sentences.md'

    with open(str(path), 'r') as fin:
        return fin.read()
