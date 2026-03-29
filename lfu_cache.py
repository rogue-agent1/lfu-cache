#!/usr/bin/env python3
"""lfu_cache - Least Frequently Used cache with O(1) operations."""
import sys
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.vals = {}
        self.freqs = {}
        self.freq_map = defaultdict(OrderedDict)
        self.min_freq = 0
    def get(self, key):
        if key not in self.vals: return None
        self._touch(key)
        return self.vals[key]
    def put(self, key, val):
        if self.cap <= 0: return
        if key in self.vals:
            self.vals[key] = val
            self._touch(key)
            return
        if len(self.vals) >= self.cap:
            evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
            del self.vals[evict_key]
            del self.freqs[evict_key]
        self.vals[key] = val
        self.freqs[key] = 1
        self.freq_map[1][key] = True
        self.min_freq = 1
    def _touch(self, key):
        f = self.freqs[key]
        del self.freq_map[f][key]
        if not self.freq_map[f]:
            del self.freq_map[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.freqs[key] = f + 1
        self.freq_map[f + 1][key] = True

def test():
    c = LFUCache(2)
    c.put("a", 1); c.put("b", 2)
    assert c.get("a") == 1  # freq(a)=2
    c.put("c", 3)  # evicts b (freq=1, least recent)
    assert c.get("b") is None
    assert c.get("c") == 3
    c.put("d", 4)  # evicts c (freq=1 < a's freq=2... but c was just accessed so freq=2; a=2, c=2, evict LRU among freq=2)
    # Actually: a=2, c=2, d=1. min_freq=1, evict d? No, d was just inserted. Let me trace:
    # After get(c): a=2, c=2. put(d): len=2>=2, min_freq=2, evict LRU of freq 2 = a
    assert c.get("a") is None
    assert c.get("d") == 4
    print("lfu_cache: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: lfu_cache.py --test")
