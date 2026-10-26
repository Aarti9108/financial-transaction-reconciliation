from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionCreate(BaseModel):
    transaction_reference: str = Field(
        min_length=1,
        max_length=100
    )
    source: str = Field(
        min_length=1,
        max_length=50
    )
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2
    )
    currency: Literal["INR", "USD", "EUR", "GBP"] = "INR"
    status: Literal["SUCCESS", "FAILED", "PENDING"]
    transaction_date: datetime

    @field_validator("transaction_reference", "source")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot contain only whitespace")
        return value

    @field_validator("currency", "status", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().upper()
        return value


class TransactionResponse(TransactionCreate):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
