from collections import defaultdict
from random import choice

class MarkovChain:
    SENTENCE_STOP = '.'

    def __init__(self):
        self.chain = defaultdict(list)
        # this will be `True` if the chain can be terminated aka.
        # if it contains a `SENTENCE_STOP`
        self.has_sentence_support = False

    # this is only used if the value to be printed is not equal to the key.
    # for naive markov chains the state name is equal to the word.
    def _lookup_value(self, state):
        return state

    def _start_state(self):
        return MarkovChain.SENTENCE_STOP

    def _random_start_state(self):
        def get_word():
            return choice(list(self.chain.keys()))

        if self.has_sentence_support:
            prev = get_word()
            while prev == MarkovChain.SENTENCE_STOP:
                prev = get_word()
            return prev

        return get_word()

    def __tokenize(self, s):
        for line in s.split('\n'):
            for word in line.split(' '):
                word = word.strip().lower()

                if not word:
                    continue

                yield word

    def add_string(self, s):
        words = list(self.__tokenize(s))
        idx = 1

        for word in words[idx:]:
            key = words[idx - 1]

            if word == MarkovChain.SENTENCE_STOP:
                self.has_sentence_support = True

            self.chain[key].append(word)

            idx += 1

    # generate a text block consisting of `s` sentences.
    def generate_text(self, s=4):
        # make sure that this chain actually contains a termination token.
        if not self.has_sentence_support:
            raise Exception(
                'Cannot generate sentences as chain does not contain '
                f'`{MarkovChain.SENTENCE_STOP}`.'
            )

        text = []

        for _ in range(s):
            prev = choice(self.chain[self._random_start_state()])

            while True:
                try:
                    state = choice(self.chain[prev])
                except IndexError:
                    state = self._random_start_state()

                text.append(self._lookup_value(state))

                # check if we reached the end of a sentence
                if state == self._start_state():
                    break

                prev = state

        return text

    # generate a sequence of `n` words
    def generate(self, n=20):
        prev = self._start_state()
        sentence = []

        for i in range(n):
            try:
                state = choice(self.chain[prev])
            except IndexError:
                state = self._random_start_state()

            sentence.append(self._lookup_value(state))

            prev = state

        return sentence
