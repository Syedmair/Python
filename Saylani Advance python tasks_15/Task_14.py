import contextlib
import json
import os
import tempfile
from pathlib import Path

DEFAULT_PATH = Path("contacts.json")


class StorageError(Exception):
    """The data file could not be read or written."""

class CorruptStorageError(StorageError):
    """The file exists but its contents are not usable. It is never overwritten."""


def load(path=DEFAULT_PATH):
    """Return {"next_id": int, "contacts": [dict, ...]}.
    A missing file means a fresh start. Anything unreadable raises, so the
    caller never ends up saving over data it could not read."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"next_id": 1, "contacts": []}
    except UnicodeDecodeError as e:
        raise CorruptStorageError(f"{path} is not valid UTF-8 text ({e})") from e
    except OSError as e:
        raise StorageError(f"Cannot read {path}: {e}") from e

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise CorruptStorageError(f"{path} is not valid JSON ({e})") from e
    return _validate(data, path)


def _validate(data, path):
    def bad(reason):
        return CorruptStorageError(f"{path} has an unexpected structure: {reason}")

    if not isinstance(data, dict) or not isinstance(data.get("contacts"), list):
        raise bad("expected an object with a 'contacts' list")

    seen = set()
    for i, c in enumerate(data["contacts"]):
        if not isinstance(c, dict):
            raise bad(f"entry {i} is not an object")
        cid = c.get("id")
        if isinstance(cid, bool) or not isinstance(cid, int) or cid < 1:
            raise bad(f"entry {i} has an invalid id")
        if cid in seen:
            raise bad(f"duplicate id {cid}")
        seen.add(cid)
        if not all(isinstance(c.get(f), str) for f in ("name", "phone", "email")):
            raise bad(f"entry {i} needs string name, phone and email")
        if not c["name"].strip():
            raise bad(f"entry {i} has an empty name")

    next_id = data.get("next_id")
    if isinstance(next_id, bool) or not isinstance(next_id, int):
        next_id = 1
    return {"next_id": max(next_id, max(seen, default=0) + 1), "contacts": data["contacts"]}


def save(data, path=DEFAULT_PATH):
    """Atomic write: write a temp file, flush it to disk, then swap it into place.
    A crash mid-save leaves the previous file intact."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException as e:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        if isinstance(e, OSError):
            raise StorageError(f"Cannot write {path}: {e}") from e
        raise