import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime

_TS_SHAPE = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
_LEVEL_SHAPE = re.compile(r"[A-Z]+")

class LogStats:
    """Filled in while a generator runs; read it after (or during) iteration."""
    lines_read: int = 0
    malformed: int = 0


def _parse(line):
    """Return (timestamp, level, message), or None if the line is malformed."""
    parts = line.split(" | ", 2)           
    if len(parts) != 3:
        return None
    ts, level, message = parts[0], parts[1], parts[2].strip()

    if not _TS_SHAPE.fullmatch(ts) or not _LEVEL_SHAPE.fullmatch(level) or not message:
        return None
    try:
        datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")   
    except ValueError:
        return None
    return ts, level, message


def read_errors(path, stats=None):
    """Stream `path` line by line, yielding (line_number, timestamp, message)
    for ERROR records only. Pass a LogStats to collect malformed-line counts."""
    if stats is None:
        stats = LogStats()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line_no, raw in enumerate(f, start=1):    
            stats.lines_read += 1
            line = raw.rstrip("\r\n")
            if not line.strip():                        
                continue
            record = _parse(line)
            if record is None:
                stats.malformed += 1
                continue
            ts, level, message = record
            if level == "ERROR":
                yield line_no, ts, message


def summarize_errors(path):
    """Count ERROR records per date and report how many lines were malformed."""
    stats = LogStats()
    counts = Counter(ts[:10] for _, ts, _ in read_errors(path, stats))
    return {
        "by_date": dict(sorted(counts.items())),
        "total_errors": sum(counts.values()),
        "malformed": stats.malformed,
    }