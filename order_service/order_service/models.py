from sqlmodel import SQLModel,Field,Relationship
from typing import Optional



class OrderItem(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    order_id:int=Field(foreign_key="order.id", nullable=False)
    product_id:int
    quantity:int
    order:Optional["Order"] = Relationship(back_populates("items"))
class Order(SQLModel,table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    user_id:int
    total_price:float
    items:List[OrderItem] = Relationship(
        back_populates = "order",
        sa_relationship_kwargs = {"cascade":"all, delete-orphan"}
        
        
    )
Order.model_rebuild()
OrderItem.model_rebuild()