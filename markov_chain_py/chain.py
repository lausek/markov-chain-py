import logging
from random import choice

try:
    from .table import LookupTable
    from .state import LookbackState

except:
    from table import LookupTable
    from state import LookbackState


class MarkovChain(object):
    SENTENCE_STOP = "."

    def __init__(self, lookback):
        self.lookback = lookback
        self.table = LookupTable(self.lookback)
        # this will be `True` if the chain can be terminated aka.
        # if it contains a `SENTENCE_STOP`
        self.has_sentence_support = False
        self.keep_newlines = False

    def _build_initial_key(self, it, lookback):
        return LookbackState(lookback, [next(it) for _ in range(lookback)])

    def _format_output_sequence(self, sequence):
        return " ".join(sequence)

    def _tokenize(self, s):
        # make sure that SENTENCE_STOP has enough space to correctly tokenize
        s = (
            s.replace(".", " . ")
            .replace(",", " , ")
            .replace("!", " ! ")
            .replace("?", " ? ")
        )

        for line in s.split("\n"):
            if self.keep_newlines:
                yield "\n"

            for word in line.split(" "):
                word = word.strip().lower()

                if not word:
                    continue

                yield word

    # this is only used if the value to be printed is not equal to the key.
    # for naive markov chains the state name is equal to the word.
    def _patch_step(self, state):
        return state, state

    def _start_state(self) -> str:
        if self.has_sentence_support:
            return MarkovChain.SENTENCE_STOP
        return self.table.find_random_state()

    def enable_keep_newlines(self):
        self.keep_newlines = True

    def add_string(self, s):
        words = iter(self._tokenize(s))
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

            state, emit = self._patch_step(state)
            sequence.append(emit)

            if termination_func((state, emit)):
                break

            prev_state.update(state)

        logging.debug("# lookback: %d", self.lookback)
        logging.debug("# top-level states: %d", len(self.table.keys()))
        logging.debug("# resets: %d", resets)
        logging.debug("")

        return sequence

    # generate a text block consisting of `s` sentences.
    def generate_text(self, s=4):
        def terminate_on_cycle(kv):
            return kv[0] == self._start_state()

        # make sure that this chain actually contains a termination token.
        if not self.has_sentence_support:
            raise Exception(
                "Cannot generate sentences as chain does not contain "
                f"`{MarkovChain.SENTENCE_STOP}`."
            )

        text = (self._generate_sequence(terminate_on_cycle) for _ in range(s))

        return " ".join(map(self._format_output_sequence, text))

    # generate a sequence of `n` words
    def generate(self, n=20):
        def terminate_on_amount():
            def inner(_kv):
                emitted_words_counter[0] += 1
                return n <= emitted_words_counter[0]

            return inner

        # implement this as list to allow sharing between functions
        emitted_words_counter = [0]

        sequence = self._generate_sequence(terminate_on_amount())
        return self._format_output_sequence(sequence)
