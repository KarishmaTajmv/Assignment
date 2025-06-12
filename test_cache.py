
from cache import create_cache
import time
import threading

def test_basic_ops():
    print("Testing basic put/get")
    cache = create_cache(max_size=3)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.delete("b")
    assert cache.get("b") is None
    cache.clear()
    assert cache.get("a") is None
    print(" basic ops passed-done")

def test_ttl_expiry():
    print("Testing TTL expiry-ok lets go")
    cache = create_cache()
    cache.put("x", "value", ttl=1)
    time.sleep(2)
    assert cache.get("x") is None
    print(" TTL expiry passed-yayyy")

def test_eviction():
    print("Testing LRU eviction")
    cache = create_cache(max_size=2)
    cache.put("x", 1)
    cache.put("y", 2)
    cache.get("x")
    cache.put("z", 3)
    assert cache.get("y") is None
    assert cache.get("x") == 1
    print("yes--- eviction passed")

def test_concurrent():
    print("Testing multithreading")
    cache = create_cache(max_size=1000)

    def worker(id):
        for i in range(100):
            key = f"{id}-{i}"
            cache.put(key, i)
            cache.get(f"{id}-{i//2}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()

    print("yippee -concurrent test passed")
    print("Stats:", cache.get_stats())

if __name__ == "__main__":
    test_basic_ops()
    test_ttl_expiry()
    test_eviction()
    test_concurrent()
