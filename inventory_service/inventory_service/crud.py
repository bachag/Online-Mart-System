from sqlmodel import Session,select
from inventory_service.models import InventoryItem
from inventory_service.schemas import InventoryItemCreate,InventoryItemRead,InventoryItemUpdate
from typing import Optional

def get_inventory_item_id(session:Session,inventory_id:int)->Optional[InventoryItem]:
    statment = select(InventoryItem).where(InventoryItem.id == inventory_id)
    return session.exec(statment).first()

def create_inventory_item(session:Session,item:InventoryItemCreate):
    db_item = InventoryItem.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_inventory_item(session:Session):
    statment = select( InventoryItem)
    return session.exec(statment).all()