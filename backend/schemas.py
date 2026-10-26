
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    transaction_reference: str = Field(min_length=1, max_length=100)
    source: str = Field(min_length=1, max_length=50)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    status: str = Field(min_length=1, max_length=30)
    transaction_date: datetime


class TransactionResponse(TransactionCreate):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
