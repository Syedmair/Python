import functools
import threading
import time
from collections import namedtuple

CacheInfo = namedtuple("CacheInfo", "hits misses size")


def ttl_cache(seconds):
    """Cache a function's results for `seconds`, keyed on its arguments."""
    if callable(seconds):
        raise TypeError("ttl_cache must be called with a duration: @ttl_cache(seconds)")
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds <= 0:
        raise ValueError("seconds must be a positive number")

    def decorator(func):
        store = {}                    
        stats = {"hits": 0, "misses": 0}
        lock = threading.Lock()

        def make_key(args, kwargs):
            key = (args, tuple(sorted(kwargs.items(), key=lambda kv: kv[0])))
            try:
                hash(key)
            except TypeError:
                raise TypeError(
                    f"{func.__name__}: ttl_cache requires hashable arguments "
                    f"(got an unhashable value in args={args!r}, kwargs={kwargs!r})"
                ) from None
            return key

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            now = time.monotonic()

            with lock:
                entry = store.get(key)
                if entry is not None and now < entry[1]:
                    stats["hits"] += 1
                    return entry[0]
                stats["misses"] += 1
                for k in [k for k, (_, exp) in store.items() if now >= exp]:
                    del store[k]

            result = func(*args, **kwargs)        
            with lock:
                store[key] = (result, time.monotonic() + seconds)
            return result

        def cache_info():
            with lock:
                return CacheInfo(stats["hits"], stats["misses"], len(store))

        def cache_clear():
            with lock:
                store.clear()
                stats["hits"] = stats["misses"] = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return decorator