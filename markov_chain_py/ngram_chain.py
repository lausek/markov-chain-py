# credits to Flash3r01

from collections import defaultdict
import logging
import os
import random

try:
    from .chain import MarkovChain

except:
    from chain import MarkovChain

class NGramMarkovChain(MarkovChain):
    def __init__(self, lookback):
        super().__init__(lookback)

    def _format_output_sequence(self, sequence):
        return ''.join(sequence)

    def _tokenize(self, s):
        if not self.keep_newlines:
            should_keep_char = lambda c: c not in ['\n']
            return iter(filter(should_keep_char, s))

        return iter(s.replace('\n', ' \n '))

    def add_string(self, s):
        chars = self._tokenize(s)
        prev = self._build_initial_key(chars, self.lookback)

        for char in chars:
            if char == MarkovChain.SENTENCE_STOP:
                self.has_sentence_support = True

            self.table.add(prev.get(), char)

            prev.update(char)
