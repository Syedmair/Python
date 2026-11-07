import csv
import re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

_NUMBER = re.compile(r"[+-]?\d+(\.\d+)?", re.ASCII)  
_GRADES = ((85, "A"), (70, "B"), (55, "C"), (40, "D"))


def _require_columns(reader, needed, path):
    if not reader.fieldnames or not needed <= set(reader.fieldnames):
        raise ValueError(f"{path}: expected columns {sorted(needed)}, found {reader.fieldnames}")


def _id_key(sid):
    """Numeric IDs sort numerically (99 before 101); anything else sorts as text after them."""
    return (0, int(sid), sid) if sid.isascii() and sid.isdigit() else (1, 0, sid)


def _grade(avg):
    for cutoff, letter in _GRADES:
        if avg >= cutoff:
            return letter
    return "F"


def _fmt(avg):
    """Round half up to 2 places, then drop one trailing zero: 85 -> '85.0', 70.5 -> '70.5'."""
    q = (Decimal(avg.numerator) / Decimal(avg.denominator)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    s = f"{q:.2f}"
    return s[:-1] if s.endswith("0") else s


def load_students(path):
    """Return {student_id: name}. This file is the source of truth, so bad rows are fatal."""
    students = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        _require_columns(reader, {"student_id", "name"}, path)
        for row in reader:
            where = f"{path} line {reader.line_num}"
            if None in row or None in row.values():
                raise ValueError(f"{where}: missing or extra fields")
            sid, name = row["student_id"].strip(), row["name"].strip()
            if not sid or not name:
                raise ValueError(f"{where}: student_id and name must not be empty")
            if sid in students:
                raise ValueError(f"{where}: duplicate student_id {sid!r}")
            students[sid] = name
    return students


def load_scores(path, students):
    """Return ({student_id: {subject: marks}}, rejected_rows). Bad rows are rejected, not fatal."""
    marks_by_student = {sid: {} for sid in students}
    rejected = []

    def reject(line, row, reason):
        rejected.append([line, row.get("student_id") or "", row.get("subject") or "",
                         row.get("marks") or "", reason])

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        _require_columns(reader, {"student_id", "subject", "marks"}, path)
        for row in reader:
            line = reader.line_num
            if None in row or None in row.values():
                reject(line, row, "Row has missing or extra fields")
                continue
            sid, subject, text = (row["student_id"].strip(), row["subject"].strip(),
                                  row["marks"].strip())
            if sid not in students:
                reject(line, row, f"Unknown student ID {sid!r}")
                continue
            if not subject:
                reject(line, row, "Subject is empty")
                continue
            if not _NUMBER.fullmatch(text):
                reject(line, row, f"Marks must be a number, got {text!r}")
                continue
            marks = Fraction(text)                      
            if not 0 <= marks <= 100:
                reject(line, row, f"Marks must be between 0 and 100, got {text!r}")
                continue
            key = subject.casefold()               
            if key in marks_by_student[sid]:
                reject(line, row, f"Duplicate entry for student {sid} in subject {subject!r}; "
                                  f"first entry kept")
                continue
            marks_by_student[sid][key] = marks
    return marks_by_student, rejected


def generate_report(students_path="students.csv", scores_path="scores.csv",
                    report_path="report.csv", rejected_path="rejected_scores.csv"):
    students = load_students(students_path)
    marks_by_student, rejected = load_scores(scores_path, students)

    ranked, unscored = [], []
    for sid, subjects in marks_by_student.items():
        if subjects:
            ranked.append((sid, sum(subjects.values()) / len(subjects), len(subjects)))
        else:
            unscored.append(sid)

    ranked.sort(key=lambda r: (-r[1], _id_key(r[0])))
    unscored.sort(key=_id_key)

    with open(report_path, "w", newline="", encoding="utf-8") as f:
        out = csv.writer(f)
        out.writerow(["rank", "student_id", "name", "subjects", "average", "grade"])
        for rank, (sid, avg, count) in enumerate(ranked, start=1):
            out.writerow([rank, sid, students[sid], count, _fmt(avg), _grade(avg)])
        for sid in unscored:                           
            out.writerow(["", sid, students[sid], 0, "", "N/A"])

    with open(rejected_path, "w", newline="", encoding="utf-8") as f:
        out = csv.writer(f)
        out.writerow(["line", "student_id", "subject", "marks", "reason"])
        out.writerows(rejected)

    return {"students": len(students), "ranked": len(ranked), "rejected": len(rejected)}