
from cache import create_cache
import time

if __name__ == "__main__":
    print("Running demo...")
    cache = create_cache(max_size=5, default_ttl=3)
    cache.put("config:api", "12345")
    print("Fetched:", cache.get("config:api"))
    time.sleep(4)
    print("Should be expired now:", cache.get("config:api"))
    cache.put("new", "val")
    print("Stats so far:", cache.get_stats())
