from sqlmodel import Field, SQLModel
from typing import List, Optional

class OrderItemBase(SQLModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(SQLModel):
    id: int
    product_id: int
    quantity: int

class OrderCreate(SQLModel):
    user_id: int
    items: List[OrderItemCreate]
    total_price: float

class OrderUpdate(SQLModel):
    user_id: Optional[int] = None
    items: Optional[List[OrderItemUpdate]] = None
    total_price: Optional[float] = None

class OrderList(SQLModel):
    id: int
    user_id: int
    total_price: float

class OrderDetail(SQLModel):
    id: int
    user_id: int
    items: List[OrderItemBase]
    total_price: float

class OrderResponse(SQLModel):
    id: int
    user_id: int
    items: List[OrderItemBase]
    total_price: float

# Ensure OrderVerify is defined
class OrderVerify(SQLModel):
    user_id: int
    total_price: float