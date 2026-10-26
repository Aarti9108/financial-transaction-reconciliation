
from backend.reconciliation import reconcile_transactions

# Transactions from Source A
source_a = [
    {
        "transaction_reference": "TXN101",
        "amount": 500,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN102",
        "amount": 800,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN103",
        "amount": 300,
        "status": "FAILED"
    },
    {
        "transaction_reference": "TXN104",
        "amount": 100,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN104",
        "amount": 100,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN105",
        "amount": 600,
        "status": "SUCCESS",
        "transaction_date": "2026-10-25"
    }
]

# Transactions from Source B
source_b = [
    {
        "transaction_reference": "TXN101",
        "amount": 500,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN102",
        "amount": 900,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN103",
        "amount": 300,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN106",
        "amount": 200,
        "status": "SUCCESS"
    },
    {
        "transaction_reference": "TXN105",
        "amount": 600,
        "status": "SUCCESS",
        "transaction_date": "2026-10-26"
    }
]

# Run reconciliation
results = reconcile_transactions(source_a, source_b)

# Display results
print("\n--- Reconciliation Results ---")

for result in results:
    print(
        f"Transaction: {result['transaction_reference']} | "
        f"Status: {result['status']}"
    )
