import threading

class SetWithLock:
    def __init__(self):
        self._set = set()
        self._lock = threading.Lock()

    def add(self, item):
        with self._lock:
            self._set.add(item)

    def remove(self, item):
        with self._lock:
            self._set.remove(item)

    def discard(self, item):
        with self._lock:
            self._set.discard(item)

    def contains(self, item):
        with self._lock:
            return item in self._set

    def clear(self):
        with self._lock:
            self._set.clear()

    def size(self):
        with self._lock:
            return len(self._set)

    def to_list(self):
        with self._lock:
            return list(self._set)

    def __contains__(self, item):
        return self.contains(item)

    def __len__(self):
        return self.size()

    def __iter__(self):
        # Snapshot iteration (copy under lock to avoid holding lock during iteration)
        with self._lock:
            return iter(self._set.copy())
