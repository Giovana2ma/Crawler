import threading

class MapWithLock:
    def __init__(self):
        self._map = {}
        self._lock = threading.Lock()

    def get(self, key, default=None):
        with self._lock:
            return self._map.get(key, default)

    def set(self, key, value):
        with self._lock:
            self._map[key] = value

    def delete(self, key):
        with self._lock:
            if key in self._map:
                del self._map[key]

    def contains(self, key):
        with self._lock:
            return key in self._map

    def keys(self):
        with self._lock:
            return list(self._map.keys())

    def values(self):
        with self._lock:
            return list(self._map.values())

    def items(self):
        with self._lock:
            return list(self._map.items())

    def clear(self):
        with self._lock:
            self._map.clear()

    def size(self):
        with self._lock:
            return len(self._map)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def __contains__(self, key):
        return self.contains(key)

    def __len__(self):
        return self.size()
