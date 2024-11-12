from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", nullable=False)
    product_id: int
    quantity: int

    # Specify back_populates on both sides of the relationship
    order: Optional["Order"] = Relationship(back_populates="items")


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    total_price: float

    # Define the relationship with OrderItem, using back_populates for bidirectional linking
    items: List[OrderItem] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# Rebuild models if necessary
Order.model_rebuild()
OrderItem.model_rebuild()