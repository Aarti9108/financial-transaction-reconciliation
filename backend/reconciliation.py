
from collections import Counter
from decimal import Decimal


def reconcile_transactions(source_a, source_b):
    results = []

    # Step 1: Count transaction references
    counts_a = Counter(
        txn["transaction_reference"] for txn in source_a
    )
    counts_b = Counter(
        txn["transaction_reference"] for txn in source_b
    )

    # Step 2: Group transactions by reference
    transactions_a = {}
    transactions_b = {}

    for txn in source_a:
        reference = txn["transaction_reference"]
        transactions_a.setdefault(reference, []).append(txn)

    for txn in source_b:
        reference = txn["transaction_reference"]
        transactions_b.setdefault(reference, []).append(txn)

    # Step 3: Collect all references
    all_references = set(transactions_a) | set(transactions_b)

    # Step 4: Reconcile each reference
    for reference in sorted(all_references):
        records_a = transactions_a.get(reference, [])
        records_b = transactions_b.get(reference, [])

        if counts_a[reference] > 1 or counts_b[reference] > 1:
            status = "DUPLICATE_TRANSACTION"

        elif not records_a:
            status = "MISSING_IN_SOURCE_A"

        elif not records_b:
            status = "MISSING_IN_SOURCE_B"

        else:
            txn_a = records_a[0]
            txn_b = records_b[0]

            if Decimal(str(txn_a["amount"])) != Decimal(str(txn_b["amount"])):
                status = "AMOUNT_MISMATCH"

            elif txn_a["status"] != txn_b["status"]:
                status = "STATUS_MISMATCH"

            elif (
                txn_a.get("transaction_date") is not None
                and txn_b.get("transaction_date") is not None
                and str(txn_a["transaction_date"])[:10]
                != str(txn_b["transaction_date"])[:10]
            ):
             status = "DATE_MISMATCH"

            else:
                status = "MATCHED"

        # Step 5: Save the result
        results.append({
            "transaction_reference": reference,
            "status": status,
        })

    return results