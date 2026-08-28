from sqlalchemy import ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import decimal
from sqlalchemy.sql.sqltypes import DateTime
from app.backend.database.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    account_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
    )

    amount: Mapped[decimal.Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    category_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("categories.category_id", ondelete="SET NULL"),
        nullable=True,
    )

    transaction_kind: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    transaction_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False, 
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
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