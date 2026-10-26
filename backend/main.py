
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.reconciliation import reconcile_transactions
from fastapi import Body

from backend.database import SessionLocal
from backend.models import Transaction, ReconciliationResult
from backend.schemas import (
    TransactionCreate,
    TransactionResponse,
    ReconciliationRequest,
)

app = FastAPI(
    title="Financial Reconciliation System",
    description="API for financial transaction reconciliation",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Financial Reconciliation System is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = Transaction(**transaction.model_dump())

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save transaction."
        )


@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.id.desc()).all()

@app.post("/reconcile")
def reconcile(
    request: ReconciliationRequest,
    db: Session = Depends(get_db)
):
    source_a = [
        txn.model_dump()
        for txn in request.source_a
    ]

    source_b = [
        txn.model_dump()
        for txn in request.source_b
    ]

    results = reconcile_transactions(source_a, source_b)

    try:
        for result in results:
            db.add(
                ReconciliationResult(
                    transaction_reference=result["transaction_reference"],
                    status=result["status"]
                )
            )

        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save reconciliation results"
        )

    return results

@app.get("/reconciliation-results")
def get_reconciliation_results(db: Session = Depends(get_db)):
    return (
        db.query(ReconciliationResult)
        .order_by(ReconciliationResult.id.desc())
        .all()
    )