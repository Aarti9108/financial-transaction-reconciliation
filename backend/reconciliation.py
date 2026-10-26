
from collections import Counter
from decimal import Decimal


def reconcile_transactions(source_a, source_b):
    results = []

    # Step 1: Detect duplicate transaction IDs
    counts_a = Counter(
        txn["transaction_reference"] for txn in source_a
    )
    counts_b = Counter(
        txn["transaction_reference"] for txn in source_b
    )

    duplicates_a = {
        ref for ref, count in counts_a.items() if count > 1
    }
    duplicates_b = {
        ref for ref, count in counts_b.items() if count > 1
    }

    # Step 2: Organize transactions by reference
    transactions_a = {
        txn["transaction_reference"]: txn for txn in source_a
    }
    transactions_b = {
        txn["transaction_reference"]: txn for txn in source_b
    }

    # Step 3: Collect all unique transaction references
    all_references = set(transactions_a) | set(transactions_b)

    # Step 4: Compare each transaction
    for reference in sorted(all_references):
        txn_a = transactions_a.get(reference)
        txn_b = transactions_b.get(reference)

        if reference in duplicates_a or reference in duplicates_b:
            status = "DUPLICATE_TRANSACTION"

        elif txn_a is None:
            status = "MISSING_IN_SOURCE_A"

        elif txn_b is None:
            status = "MISSING_IN_SOURCE_B"

        elif Decimal(str(txn_a["amount"])) != Decimal(str(txn_b["amount"])):
            status = "AMOUNT_MISMATCH"

        elif txn_a["status"] != txn_b["status"]:
            status = "STATUS_MISMATCH"

        elif (
            txn_a.get("transaction_date") is not None
            and txn_b.get("transaction_date") is not None
            and txn_a["transaction_date"] != txn_b["transaction_date"]
        ):
            status = "DATE_MISMATCH"

        else:
            status = "MATCHED"

        # Step 5: Store the result
        results.append({
            "transaction_reference": reference,
            "status": status
        })

    return results
