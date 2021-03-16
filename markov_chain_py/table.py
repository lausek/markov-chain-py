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

    def keys(self):
        return self._layer.keys()

    def get(self, key):
        assert len(key) <= self._depth

        if len(key) == self._depth:
            if 1 < self._depth:
                return self._layer[key[0]].get(key[1:])
            return self._layer[key[0]]

        # key is too short, brute force through child layers
        for child_layer in self._layer.values():
            try:
                return child_layer.get(key)
            except IndexError:
                pass

        raise IndexError()

    def add(self, key, item):
        assert len(key) <= self._depth

        if len(key) == self._depth:
            # this layer is nested
            if 1 < self._depth:
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

    def __repr__(self):
        return str(self._layer)
