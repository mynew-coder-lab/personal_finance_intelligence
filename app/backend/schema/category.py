from pydantic import BaseModel, ConfigDict, Field, field_validator
import datetime
from typing import Literal

CategoryTypeLiteral = Literal["income", "expense"]


class CategoryCreateRequest(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=100)
    category_type: CategoryTypeLiteral
    parent_category_id: int | None = Field(default=None)

    @field_validator("category_name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Category name cannot be empty or whitespace only")
        return stripped


class CategoryResponse(BaseModel):
    category_id: int
    user_id: int
    category_name: str
    category_type: str
    parent_category_id: int | None
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
