class LookupTable:
    def __init__(self, graceful=True):
        self._inner = {}
        self._graceful = graceful

    def __normalize_key(self, key):
        if isinstance(key, list) or isinstance(key, tuple):
            return list(map(str, key))

        if isinstance(key, str):
            return [key]

        raise Exception("key of type %s is not supported" % type(key).__name__)

    def keys(self):
        return self._inner.keys()

    def get(self, key):
        key = self.__normalize_key(key)
        current_layer = self._inner

        for key_part in key:
            if key_part not in current_layer:
                raise IndexError()

            current_layer = current_layer[key_part]

        return current_layer

    def add(self, key, item):
        key = self.__normalize_key(key)
        last_layer_idx = len(key) - 1
        current_layer = self._inner

        for idx, key_part in enumerate(key):
            if idx == last_layer_idx:
                if key_part not in current_layer:
                    current_layer[key_part] = []

                current_layer[key_part].append(item)

            else:
                if key_part not in current_layer:
                    current_layer[key_part] = {}

                current_layer = current_layer[key_part]
