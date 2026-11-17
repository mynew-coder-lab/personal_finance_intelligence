from pydantic import BaseModel, ConfigDict, Field, field_validator
import datetime
from decimal import Decimal
from typing import Literal

VALID_ACCOUNT_TYPES = ("checking", "savings", "credit_card", "cash", "investment", "loan")
VALID_CURRENCIES = ("USD", "EUR", "GBP", "JPY", "CAD", "AUD")

AccountTypeLiteral = Literal["checking", "savings", "credit_card", "cash", "investment", "loan"]
CurrencyLiteral = Literal["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]


class AccountCreateRequest(BaseModel):
    account_name: str = Field(..., min_length=1, max_length=100)
    account_type: AccountTypeLiteral
    currency: CurrencyLiteral
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0)

    @field_validator("account_name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Account name cannot be empty or whitespace only")
        return stripped

    @field_validator("opening_balance")
    @classmethod
    def round_balance(cls, value: Decimal) -> Decimal:
        return round(value, 2)


class AccountResponse(BaseModel):
    account_id: int
    user_id: int
    account_name: str
    account_type: str
    currency: str
    opening_balance: Decimal
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
