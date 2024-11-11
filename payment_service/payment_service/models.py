from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id:int
    amount:float
    status:str
    client_secret:Optional[str] = None