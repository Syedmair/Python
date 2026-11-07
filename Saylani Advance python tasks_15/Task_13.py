import bisect
from dataclasses import dataclass
from datetime import datetime


class SchedulerError(ValueError):
    pass

class InvalidBookingError(SchedulerError):
    pass

class DuplicateBookingError(SchedulerError):
    pass


@dataclass(frozen=True)
class Booking:
    id: object
    room: object
    start: datetime
    end: datetime            


@dataclass(frozen=True)
class BookingResult:
    accepted: bool
    booking: Booking
    conflicts: tuple = ()    


def _is_aware(dt):
    return dt.tzinfo is not None and dt.utcoffset() is not None


class RoomScheduler:
    def __init__(self):
        self._by_id = {}      
        self._ends = {}      
        self._items = {}      
        self._aware = None    

    def book(self, booking_id, room, start, end):
        """Accept the booking or return the conflicts. Invalid input raises."""
        self._validate(booking_id, start, end)
        booking = Booking(booking_id, room, start, end)

        ends = self._ends.setdefault(room, [])
        items = self._items.setdefault(room, [])
        i = bisect.bisect_right(ends, start)
        j = i
        while j < len(items) and items[j].start < end:
            j += 1
        if j > i:
            return BookingResult(False, booking, tuple(items[i:j]))

        ends.insert(i, end)
        items.insert(i, booking)
        self._by_id[booking_id] = booking
        self._aware = _is_aware(start)
        return BookingResult(True, booking)

    def cancel(self, booking_id):
        try:
            b = self._by_id.pop(booking_id)
        except KeyError:
            raise KeyError(f"No booking with id {booking_id!r}") from None
        i = bisect.bisect_left(self._ends[b.room], b.end)    
        del self._ends[b.room][i]
        del self._items[b.room][i]
        return b

    def bookings_for(self, room):
        return tuple(self._items.get(room, ()))            
    def _validate(self, booking_id, start, end):
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise TypeError("start and end must be datetime objects")
        if _is_aware(start) != _is_aware(end):
            raise InvalidBookingError("start and end must both be naive or both timezone-aware")
        if self._aware is not None and _is_aware(start) != self._aware:
            raise InvalidBookingError("cannot mix naive and timezone-aware datetimes in one scheduler")
        if end <= start:
            raise InvalidBookingError(f"end ({end}) must be after start ({start})")
        if booking_id in self._by_id:
            raise DuplicateBookingError(f"Booking id {booking_id!r} already exists")