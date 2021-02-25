from collections import defaultdict
from random import choice

class MarkovChain:
    SENTENCE_STOP = '.'

    def __init__(self):
        self.chain = defaultdict(list)
        # this will be `True` if the chain can be terminated aka.
        # if it contains a `SENTENCE_STOP`
        self.has_sentence_support = False

    def __tokenize(self, s):
        for line in s.split('\n'):
            for word in line.split(' '):
                word = word.strip().lower()

                if not word:
                    continue

                yield word

    def __random_start_word(self):
        def get_word():
            return choice(list(self.chain.keys()))

        if self.has_sentence_support:
            prev = get_word()
            while prev == MarkovChain.SENTENCE_STOP:
                prev = get_word()
            return prev

        return get_word()

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
            prev = choice(self.chain[MarkovChain.SENTENCE_STOP])

            while True:
                word = choice(self.chain[prev])

                text.append(word)

                # check if we reached the end of a sentence
                if word == MarkovChain.SENTENCE_STOP:
                    break

                if word in self.chain:
                    prev = word
                else:
                    prev = self.__random_start_word()

        return text

    # generate a sequence of `n` words
    def generate(self, n=20):
        prev = self.__random_start_word()
        sentence = []

        for i in range(n):
            word = choice(self.chain[prev])

            sentence.append(word)

            # check that the next word has a successor
            if word in self.chain:
                prev = word
            else:
                prev = self.__random_start_word()

        return sentence
