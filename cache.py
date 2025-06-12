
import time
import threading

class CacheEntry:
    def __init__(self, key, value, ttl=None):
        self.key = key
        self.value = value
        self.timestamp = time.time()
        self.ttl = ttl
        self.prev = None
        self.next = None

    def is_expired(self):
        if self.ttl is None:
            return False
        return time.time() > self.timestamp + self.ttl

class ThreadSafeLRUCache:
    def __init__(self, max_size=1000, default_ttl=None):
        self.lock = threading.RLock()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = dict()
        self.head = None
        self.tail = None
        self.stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0,
            "evictions": 0,
            "expired_removals": 0
        }

        # cleaner thread to delete expired entries every 5 seconds
        self.stop_cleaner = False
        self.cleaner_thread = threading.Thread(target=self._cleanup, daemon=True)
        self.cleaner_thread.start()

    def _remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next
        if self.tail == node:
            self.tail = node.prev
        node.prev = node.next = None

    def _add_to_front(self, node):
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def put(self, key, value, ttl=None):
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                node.value = value
                node.timestamp = time.time()
                node.ttl = ttl or self.default_ttl
                self._move_to_front(node)
            else:
                if len(self.cache) >= self.max_size:
                    # remove the last (least recently used) node
                    if self.tail:
                        self.cache.pop(self.tail.key, None)
                        self._remove_node(self.tail)
                        self.stats["evictions"] += 1
                node = CacheEntry(key, value, ttl or self.default_ttl)
                self._add_to_front(node)
                self.cache[key] = node

    def get(self, key):
        with self.lock:
            self.stats["total_requests"] += 1
            node = self.cache.get(key)
            if not node:
                self.stats["misses"] += 1
                return None
            if node.is_expired():
                self._remove_node(node)
                del self.cache[key]
                self.stats["misses"] += 1
                self.stats["expired_removals"] += 1
                return None
            self._move_to_front(node)
            self.stats["hits"] += 1
            return node.value

    def delete(self, key):
        with self.lock:
            node = self.cache.get(key)
            if node:
                self._remove_node(node)
                del self.cache[key]

    def clear(self):
        with self.lock:
            self.cache.clear()
            self.head = None
            self.tail = None

    def get_stats(self):
        with self.lock:
            total = self.stats["total_requests"]
            hits = self.stats["hits"]
            return {
                **self.stats,
                "current_size": len(self.cache),
                "hit_rate": round(hits / total, 3) if total > 0 else 0.0
            }

    def _cleanup(self):
        while not self.stop_cleaner:
            with self.lock:
                keys_to_remove = []
                for key, node in list(self.cache.items()):
                    if node.is_expired():
                        keys_to_remove.append(key)
                for key in keys_to_remove:
                    self._remove_node(self.cache[key])
                    del self.cache[key]
                    self.stats["expired_removals"] += 1
            time.sleep(5)

    def shutdown(self):
        self.stop_cleaner = True
        self.cleaner_thread.join()

# helper to create the cache
def create_cache(max_size=1000, default_ttl=None):
    return ThreadSafeLRUCache(max_size, default_ttl)
