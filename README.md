
# Thread-Safe In-Memory Cache (SDE-1 Assignment – SatSure)

Hey there 
This is my attempt at building a lightweight, in-memory, thread-safe cache system in Python with LRU eviction and TTL support. Not gonna lie, it was a fun one.
---
## How to Run
Make sure you have Python 3.7+ installed.
```bash
python3 test_cache.py
```
please check the demo:
```bash
python3 demo.py
```
---
## Features

* LRU eviction (O(1)) using doubly linked list
* TTL-based expiration (per-entry + default)
* Thread-safe access using locks
* Background thread to auto-clean expired entries
* Tracks stats like hit rate, evictions, etc.
---
## design choice i used

- Used a dictionary for O(1) lookup
- Doubly linked list for LRU ordering
- TTL checked both during get() and via background thread
- Reentrant lock (RLock) to prevent deadlocks (some part I wasn't sure about but seems to work fine)
---
##  Concurrency Model
Just used `threading.RLock()` around every cache operation. Maybe there's a more optimal way, but this works for now and keeps things safe under multiple threads.

----------------------------------------------------------

##  Sample Stats Output
```json
{ qAS
  "hits": 5,
  "misses": 2,
  "hit_rate": 0.714,
  "total_requests": 7,
  "current_size": 3,
  "evictions": 1,
  "expired_removals": 2
}
```
-----------------------------------------------------------
## Test Cases can be 
- Basic put/get/delete/clear
- TTL expiration
- LRU eviction on size limit
- Threaded concurrent access
-------------------------------------------------------------

####

I’ve kept the implementation basic, added comments here and there (some informal too lol), but it should work well. Hit me up if something breaks or feels off 

