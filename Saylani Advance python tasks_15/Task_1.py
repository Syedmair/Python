from collections import defaultdict

def build_report(transactions):
    # 1. Reject duplicate IDs (checked across all transactions, failed included)
    seen = set()
    for t in transactions:
        if t["id"] in seen:
            raise ValueError(f"Duplicate transaction id: {t['id']}")
        seen.add(t["id"])

    # 2. Every customer gets an entry, so those with only failed
    #    transactions still appear with total 0
    spend = {t["customer"]: defaultdict(int) for t in transactions}
    for t in transactions:
        if t["status"] == "success":
            spend[t["customer"]][t["category"]] += t["amount"]

    # 3. Build rows; top category = highest spend, ties broken alphabetically
    rows = [
        {
            "customer": c,
            "total": sum(cats.values()),
            "top_category": min(cats, key=lambda k: (-cats[k], k)) if cats else None,
        }
        for c, cats in spend.items()
    ]

    # 4. Sort: spending descending, then customer name ascending
    rows.sort(key=lambda r: (-r["total"], r["customer"]))

    # 5. Rank (customers with equal totals share a rank: 1, 2, 2, 4)
    for i, r in enumerate(rows):
        same_as_prev = i > 0 and rows[i - 1]["total"] == r["total"]
        r["rank"] = rows[i - 1]["rank"] if same_as_prev else i + 1

    return rows
