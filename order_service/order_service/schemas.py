from sqlmodel import SQLModel,Field
from typing import Optional


class ProductBase(SQLModel):
    name:str
    description:Optional[str]
    price:float
    
class ProductCreate(ProductBase):
    pass
class ProductRead(ProductBase):
    id:int = Field(default=None, primary_key=True)