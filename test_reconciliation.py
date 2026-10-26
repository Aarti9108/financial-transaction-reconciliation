from backend.reconciliation import reconcile_transactions


def test_matching_transactions():
    source_a = [
        {
            "transaction_reference": "TXN101",
            "amount": 500,
            "status": "SUCCESS",
        }
    ]

    source_b = [
        {
            "transaction_reference": "TXN101",
            "amount": 500,
            "status": "SUCCESS",
        }
    ]

    results = reconcile_transactions(source_a, source_b)

    assert results == [
        {
            "transaction_reference": "TXN101",
            "status": "MATCHED",
        }
    ]


def test_amount_mismatch():
    source_a = [
        {
            "transaction_reference": "TXN102",
            "amount": 500,
            "status": "SUCCESS",
        }
    ]

    source_b = [
        {
            "transaction_reference": "TXN102",
            "amount": 700,
            "status": "SUCCESS",
        }
    ]

    results = reconcile_transactions(source_a, source_b)

    assert results[0]["status"] == "AMOUNT_MISMATCH"


def test_duplicate_transaction():
    source_a = [
        {
            "transaction_reference": "TXN103",
            "amount": 300,
            "status": "SUCCESS",
        },
        {
            "transaction_reference": "TXN103",
            "amount": 300,
            "status": "SUCCESS",
        },
    ]

    source_b = [
        {
            "transaction_reference": "TXN103",
            "amount": 300,
            "status": "SUCCESS",
        }
    ]

    results = reconcile_transactions(source_a, source_b)

    assert results[0]["status"] == "DUPLICATE_TRANSACTION"


def test_missing_transaction():
    source_a = []

    source_b = [
        {
            "transaction_reference": "TXN104",
            "amount": 200,
            "status": "SUCCESS",
        }
    ]

    results = reconcile_transactions(source_a, source_b)

    assert results[0]["status"] == "MISSING_IN_SOURCE_A"

def test_status_mismatch():
    source_a = [
        {
            "transaction_reference": "TXN105",
            "amount": 500,
            "status": "SUCCESS",
        }
    ]

    source_b = [
        {
            "transaction_reference": "TXN105",
            "amount": 500,
            "status": "FAILED",
        }
    ]

    results = reconcile_transactions(source_a, source_b)

    assert results[0]["status"] == "STATUS_MISMATCH"


def test_date_mismatch():
    source_a = [
        {
            "transaction_reference": "TXN106",
            "amount": 500,
            "status": "SUCCESS",
            "transaction_date": "2026-10-25",
        }
    ]

    source_b = [
        {
            "transaction_reference": "TXN106",
            "amount": 500,
            "status": "SUCCESS",
            "transaction_date": "2026-10-26",
        }
    ]

    results = reconcile_transactions(source_a, source_b)

    assert results[0]["status"] == "DATE_MISMATCH"