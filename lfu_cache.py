#!/usr/bin/env python3
"""lfu_cache - Least Frequently Used cache with O(1) operations."""
import sys
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.min_freq = 0
        self.key_val = {}
        self.key_freq = {}
        self.freq_keys = defaultdict(OrderedDict)

    def get(self, key):
        if key not in self.key_val:
            return None
        self._increment_freq(key)
        return self.key_val[key]

    def put(self, key, value):
        if self.capacity <= 0:
            return
        if key in self.key_val:
            self.key_val[key] = value
            self._increment_freq(key)
            return
        if len(self.key_val) >= self.capacity:
            self._evict()
        self.key_val[key] = value
        self.key_freq[key] = 1
        self.freq_keys[1][key] = True
        self.min_freq = 1

    def _increment_freq(self, key):
        freq = self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_freq[key] = freq + 1
        self.freq_keys[freq + 1][key] = True

    def _evict(self):
        keys = self.freq_keys[self.min_freq]
        evict_key, _ = keys.popitem(last=False)
        if not keys:
            del self.freq_keys[self.min_freq]
        del self.key_val[evict_key]
        del self.key_freq[evict_key]

    def size(self):
        return len(self.key_val)

def test():
    c = LFUCache(3)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") == 1
    assert c.get("a") == 1
    assert c.get("b") == 2
    c.put("d", 4)
    assert c.get("c") is None
    assert c.get("d") == 4
    assert c.get("a") == 1
    c.put("e", 5)
    assert c.get("b") is None
    assert c.size() == 3
    c2 = LFUCache(1)
    c2.put("x", 10)
    assert c2.get("x") == 10
    c2.put("y", 20)
    assert c2.get("x") is None
    assert c2.get("y") == 20
    c3 = LFUCache(0)
    c3.put("z", 1)
    assert c3.get("z") is None
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("lfu_cache: LFU cache. Use --test")
