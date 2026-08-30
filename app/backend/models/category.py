from sqlalchemy import CheckConstraint, Integer, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from sqlalchemy.sql.sqltypes import DateTime
from app.backend.database.database import Base  

class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    category_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    parent_category_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("categories.category_id", ondelete="SET NULL"),
        nullable=True,
    )
    __table_args__ = (
        CheckConstraint("category_name != ''", name="ck_category_name_not_empty"),
        CheckConstraint("parent_category_id IS NULL OR parent_category_id != category_id", name="ck_parent_category_not_self"),
    ) 
