class LookbackState:
    def __init__(self, lookback, initial):
        self.lookback = lookback

        if isinstance(initial, LookbackState):
            initial = initial._inner

        if isinstance(initial, list):
            self._inner = initial
        else:
            self._inner = list(map(str, initial))

    def __eq__(self, other):
        if not isinstance(other, LookbackState):
            raise Exception('%s is not a LookbackState' % type(other).__name__)

        return all(map(lambda pair: pair[0] == pair[1], zip(self._inner, other._inner)))

    def get(self) -> list:
        return self._inner

    def reset(self):
        self._inner = []

    def update(self, new):
        self._inner.append(new)

        if self.lookback < len(self._inner):
            self._inner.pop(0)

            assert self.lookback == len(self._inner)
