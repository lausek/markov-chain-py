from collections import defaultdict
import os
import random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import spacy

try:
    from .chain import MarkovChain
except:
    from chain import MarkovChain

class SpacyMarkovChain(MarkovChain):
    def __init__(self, model, lookback):
        super().__init__()
        self.words = defaultdict(list)
        self.lookback = lookback
        self._nlp = spacy.load(model)

    def __contains_only_punctuation(self, value):
        is_non_punctuation = lambda c: c not in ['/', '\\', '|', '-', '[', ']', '(', ')', '\n']
        return not any(map(is_non_punctuation, value))

    def _lookup_value(self, state):
        return random.choice(self.words[state])

    def _start_state(self):
        return 'PUNCT'

    def _random_start_state(self):
        return self._start_state()

    def _populate_chain(self, prev, current):
        prev_key = list(map(self._lookup_key, prev))
        current_key = self._lookup_key(current)
        self.table.add(prev_key, current_key)

    def __build_initial_key(self, it, lookback):
        return [next(it) for _ in range(lookback)]

    def add_string(self, s):
        tokens = iter(self._nlp(s))
        
        prev = self.__build_initial_key(tokens, self.lookback)
        for token in tokens:
            if self.__contains_only_punctuation(token.norm_):
                continue

            self._populate_chain(prev, token)
            self.words[self._lookup_key(token)].append(token.norm_)

            if self._lookup_key(token) == self._start_state():
                self.has_sentence_support = True

            # shift key components to the left dropping the first item
            # to satisfy `len(key) == self.lookback`
            prev.append(token)
            prev.pop(0)


class SpacyPosMarkovChain(SpacyMarkovChain):
    def __init__(self, model, lookback):
        super().__init__(model, lookback)

    def _lookup_key(self, obj):
        return obj.pos_


class SpacyTagMarkovChain(SpacyPosMarkovChain):
    def __init__(self, model, lookback):
        super().__init__(model, lookback)
        self.specialized_chain = defaultdict(list)

    def _start_state(self):
        return '$.'

    def _populate_chain(self, prev, current):
        super()._populate_chain(prev, current)

        self.specialized_chain[prev.tag_].append(current.tag_)

    def _lookup_key(self, obj):
        return obj.tag_
