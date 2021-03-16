# credits to Flash3r01

from collections import defaultdict
import logging
import os
import random

try:
    from .chain import MarkovChain
    from .state import LookbackState

except:
    from chain import MarkovChain
    from state import LookbackState

class NGramMarkovChain(MarkovChain):
    def __init__(self, lookback):
        super().__init__(lookback)

    def _format_output_sequence(self, sequence):
        return ''.join(sequence)

    def _tokenize(self, s):
        should_avoid_char = lambda c: c not in ['\n']
        return iter(filter(should_avoid_char, s))

    def add_string(self, s):
        chars = self._tokenize(s)
        prev = self._build_initial_key(chars, self.lookback)

        for char in chars:
            if char == MarkovChain.SENTENCE_STOP:
                self.has_sentence_support = True

            self.table.add(prev.get(), char)

            prev.update(char)
