from collections import defaultdict
from random import choice

class MarkovChain:
    def __init__(self):
        self.chain = defaultdict(list)

    def __tokenize(self, s):
        return [word.strip().lower() for word in s.split(' ') if word.strip()]

    def __random_start_word(self):
        return choice(list(self.chain.keys()))

    def add_string(self, s):
        words = self.__tokenize(s)
        idx = 1

        for word in words[idx:]:
            key = words[idx - 1]

            self.chain[key].append(word)

            idx += 1

    def generate(self, n=20):
        sentence = []

        prev = self.__random_start_word()
        for i in range(n):
            word = choice(self.chain[prev])

            sentence.append(word)

            # check that the next word has a successor
            if word in self.chain:
                prev = word
            else:
                prev = self.__random_start_word()

        return sentence
