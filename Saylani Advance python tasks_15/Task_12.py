import operator


class ReversibleRange:
    """A lazy, re-iterable range supporting reversed(), len(), and `in`.
    Nothing is stored except start, stop, and step."""

    __slots__ = ("_start", "_stop", "_step", "_len")

    def __init__(self, start, stop, step=1):
        self._start = operator.index(start)
        self._stop = operator.index(stop)
        self._step = operator.index(step)
        if self._step == 0:
            raise ValueError("step must not be zero")
        if self._step > 0:
            span, size = self._stop - self._start, self._step
        else:
            span, size = self._start - self._stop, -self._step
        self._len = (span + size - 1) // size if span > 0 else 0
    @property
    def start(self): return self._start
    @property
    def stop(self): return self._stop
    @property
    def step(self): return self._step
    def __iter__(self):
        cur, step, stop = self._start, self._step, self._stop
        if step > 0:
            while cur < stop:
                yield cur
                cur += step
        else:
            while cur > stop:
                yield cur
                cur += step

    def __reversed__(self):
        n = self._len
        if n == 0:
            return
        cur = self._start + (n - 1) * self._step      
        while n:
            yield cur
            cur -= self._step
            n -= 1

    def __len__(self):
        return self._len                              

    def __contains__(self, value):
        if isinstance(value, float):
            if not value.is_integer():
                return False
            value = int(value)
        elif not isinstance(value, int):
            return False

        start, stop, step = self._start, self._stop, self._step
        if step > 0:
            in_bounds = start <= value < stop
        else:
            in_bounds = stop < value <= start
        return in_bounds and (value - start) % step == 0

    def __repr__(self):
        return f"ReversibleRange({self._start}, {self._stop}, {self._step})"