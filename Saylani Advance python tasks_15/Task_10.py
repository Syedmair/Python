import csv
import re

_INT = re.compile(r"[+-]?\d+", re.ASCII)  


def _require_columns(reader, needed, path):
    if not reader.fieldnames or not needed <= set(reader.fieldnames):
        raise ValueError(f"{path}: expected columns {sorted(needed)}, found {reader.fieldnames}")


def load_inventory(path):
    """Return (stock, names). The inventory is the source of truth, so bad rows here are fatal."""
    stock, names = {}, {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        _require_columns(reader, {"sku", "name", "quantity"}, path)
        for row in reader:
            where = f"{path} line {reader.line_num}"
            if None in row or None in row.values():
                raise ValueError(f"{where}: missing or extra fields")
            sku, qty = row["sku"].strip(), row["quantity"].strip()
            if not sku:
                raise ValueError(f"{where}: empty SKU")
            if sku in stock:
                raise ValueError(f"{where}: duplicate SKU {sku!r}")
            if not _INT.fullmatch(qty) or int(qty) < 0:
                raise ValueError(f"{where}: quantity must be a non-negative integer, got {qty!r}")
            stock[sku], names[sku] = int(qty), row["name"]
    return stock, names


def _apply(row, stock):
    """Apply one movement to `stock`. Return None on success, or a rejection reason."""
    if None in row or None in row.values():
        return "Row has missing or extra fields"
    sku = row["sku"].strip()
    mtype = row["type"].strip().upper()
    units_text = row["units"].strip()

    if sku not in stock:
        return f"Unknown SKU {sku!r}"
    if mtype not in ("IN", "OUT"):
        return f"Invalid movement type {row['type'].strip()!r}"
    if not _INT.fullmatch(units_text) or int(units_text) <= 0:
        return f"Units must be a positive integer, got {units_text!r}"

    units = int(units_text)
    if mtype == "OUT":
        if units > stock[sku]:
            return f"OUT of {units} exceeds stock {stock[sku]}"
        stock[sku] -= units
    else:
        stock[sku] += units
    return None


def process_inventory(inventory_path="inventory.csv",
                      movements_path="movements.csv",
                      updated_path="updated_inventory.csv",
                      rejected_path="rejected_movements.csv"):
    stock, names = load_inventory(inventory_path)
    applied = rejected = 0

    with open(movements_path, newline="", encoding="utf-8-sig") as mf, \
         open(rejected_path, "w", newline="", encoding="utf-8") as rf:
        reader = csv.DictReader(mf)
        _require_columns(reader, {"sku", "type", "units"}, movements_path)
        out = csv.writer(rf)
        out.writerow(["line", "sku", "type", "units", "reason"])

        for row in reader:                             
            reason = _apply(row, stock)
            if reason is None:
                applied += 1
            else:
                rejected += 1
                out.writerow([reader.line_num, row.get("sku") or "",
                              row.get("type") or "", row.get("units") or "", reason])

    with open(updated_path, "w", newline="", encoding="utf-8") as uf:
        out = csv.writer(uf)
        out.writerow(["sku", "name", "quantity"])
        for sku, qty in stock.items():                  
            out.writerow([sku, names[sku], qty])

    return {"applied": applied, "rejected": rejected}