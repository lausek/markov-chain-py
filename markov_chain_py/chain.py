import logging
from random import choice

try:
    from .table import LookupTable
    from .state import LookbackState

except:
    from table import LookupTable
    from state import LookbackState

class MarkovChain(object):
    SENTENCE_STOP = '.'

    def __init__(self, lookback):
        self.lookback = lookback
        self.table = LookupTable(self.lookback)
        # this will be `True` if the chain can be terminated aka.
        # if it contains a `SENTENCE_STOP`
        self.has_sentence_support = False

    def _build_initial_key(self, it, lookback):
        return LookbackState(lookback, [next(it) for _ in range(lookback)])

    def __tokenize(self, s):
        for line in s.split('\n'):
            for word in line.split(' '):
                word = word.strip().lower()

                if not word:
                    continue

                yield word

    # this is only used if the value to be printed is not equal to the key.
    # for naive markov chains the state name is equal to the word.
    def _lookup_value(self, state):
        return state

    def _start_state(self) -> str:
        if self.has_sentence_support:
            return MarkovChain.SENTENCE_STOP
        return self.table.find_random_state()
    
    def add_string(self, s):
        words = iter(self.__tokenize(s))
        prev = self._build_initial_key(words, self.lookback)

        for word in words:
            if word == MarkovChain.SENTENCE_STOP:
                self.has_sentence_support = True

            self.table.add(prev.get(), word)

            prev.update(word)

    def _generate_sequence(self, termination_func):
        prev_state = LookbackState(self.lookback, [self._start_state()])
        sequence = []
        resets = 0

        while True:
            try:
                state = choice(self.table.get(prev_state.get()))
            except KeyError:
                # rerun with starting state
                prev_state.reset()
                prev_state.update(self._start_state())
                state = choice(self.table.get(prev_state.get()))

                resets += 1

            emitted = self._lookup_value(state)
            sequence.append(emitted)

            if termination_func((state, emitted)):
                break

            prev_state.update(state)

        logging.debug('# lookback: %d', self.lookback)
        logging.debug('# top-level states: %d', len(self.table.keys()))
        logging.debug('# resets: %d', resets)
        logging.debug('')

        return sequence

    # generate a text block consisting of `s` sentences.
    def generate_text(self, s=4):
        def terminate_on_cycle(kv):
            return kv[0] == self._start_state()


        # make sure that this chain actually contains a termination token.
        if not self.has_sentence_support:
            raise Exception(
                'Cannot generate sentences as chain does not contain '
                f'`{MarkovChain.SENTENCE_STOP}`.'
            )


        text = []

        for _ in range(s):
            text.extend(self._generate_sequence(terminate_on_cycle))

        return text

    # generate a sequence of `n` words
    def generate(self, n=20):
        def terminate_on_amount():
            def inner(_kv):
                emitted_words_counter[0] += 1
                return 20 <= emitted_words_counter[0]
            return inner


        # implement this as list to allow sharing between functions
        emitted_words_counter = [0]

        return self._generate_sequence(terminate_on_amount())
