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
        self.table = LookupTable()
        self.lookback = lookback
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

    def _start_state(self):
        return MarkovChain.SENTENCE_STOP

    def add_string(self, s):
        words = list(self.__tokenize(s))
        idx = 1

        for word in words[idx:]:
            key = words[idx - 1]

            if word == MarkovChain.SENTENCE_STOP:
                self.has_sentence_support = True

            self.table.add(key, word)

            idx += 1

    def _generate_sequence(self, termination_func):
        restart_state = lambda: LookbackState(self.lookback, self._start_state())
        prev = restart_state()
        sequence = []

        while True:
            try:
                state = choice(self.table.get(prev.get()))
            except IndexError:
                state = restart_state()

            emitted = self._lookup_value(state)
            sequence.append(emitted)

            if termination_func((state, emitted)):
                break

            prev.update(state)

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
