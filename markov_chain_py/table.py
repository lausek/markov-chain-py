import random

class Rule:
    def __init__(self, n0_states, n1_states):
        self.n0_states = n0_states
        self.n1_states = n1_states

    def prepend_n0_state(self, key):
        self.n0_states.insert(0, key)
        return self

    def __str__(self):
        from_states = ', '.join(self.n0_states)
        into_states = ' | '.join(self.n1_states)
        return f'{from_states} => {into_states}'

class LookupTable:
    def __init__(self, depth, graceful=True):
        self._depth = depth
        self._layer = {}
        self._graceful = graceful

    def __normalize_key(self, key):
        if isinstance(key, list) or isinstance(key, tuple):
            return list(map(str, key))

        if isinstance(key, str):
            return [key]

        raise Exception('key of type %s is not supported' % type(key).__name__)

    def is_nested(self):
        return 1 < self._depth

    def keys(self):
        return list(self._layer.keys())

    def find_random_state(self):
        if self.is_nested():
            return random.choice(list(self._layer.values())).find_random_state()
        return random.choice(self.keys())

    def get(self, key):
        assert len(key) <= self._depth

        if len(key) == self._depth:
            if 1 < self._depth:
                return self._layer[key[0]].get(key[1:])
            return self._layer[key[0]]

        # key is too short, brute force through child layers
        children = list(self._layer.values())
        random.shuffle(children)

        for child_layer in children:
            try:
                return child_layer.get(key)
            except KeyError:
                pass

        raise KeyError()

    def add(self, key, item):
        assert len(key) <= self._depth

        if len(key) == self._depth:
            # this layer is nested
            if self.is_nested():
                if key[0] not in self._layer:
                    self._layer[key[0]] = LookupTable(self._depth - 1)

                self._layer[key[0]].add(key[1:], item)
            
            # this layer is flat
            else:
                if key[0] not in self._layer:
                    self._layer[key[0]] = []

                self._layer[key[0]].append(item)

        else:
            for child_layer in self._layer.values():
                child_layer.add(key, item)

    def rules(self) -> list:
        if self.is_nested():
            return (rule.prepend_n0_state(key) for key, child in self._layer.items() for rule in child.rules())
        return (Rule([key], values) for key, values in self._layer.items())

    def __repr__(self):
        return '\n'.join(map(str, self.rules()))
