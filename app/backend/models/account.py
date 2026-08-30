from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import decimal
from sqlalchemy.sql.sqltypes import DateTime
from app.backend.database.database import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    account_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    account_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    opening_balance: Mapped[decimal.Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint("account_name != ''", name="ck_account_name_not_empty"),
        CheckConstraint("account_type IN ('checking', 'savings', 'credit_card', 'cash', 'investment', 'loan')", name="ck_valid_account_type"),
        CheckConstraint("currency IN ('USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD')", name="ck_valid_currency"),
        CheckConstraint("opening_balance >= 0", name="ck_opening_balance_non_negative"),
    )