from sqlmodel import SQLModel,Field
from typing import Optional


class InventoryItemCreate(SQLModel):
    product_id:int
    quantity:int
    
    
class InventoryItemRead(InventoryItemCreate):
    id:int
class InventoryItemUpdate(InventoryItemCreate):
    product_id:Optional[int] = None
    quantity:Optional[int] = None