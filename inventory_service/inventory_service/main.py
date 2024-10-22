from fastapi import FastAPI,HTTPException,Depends
from sqlmodel import Session
from inventory_service.db import create_db_and_tables,get_session
from inventory_service.schemas import InventoryItemCreate,InventoryItemRead
from inventory_service.crud import create_inventory_item,get_inventory_item,get_inventory_item_id
from typing import Optional 
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/Inventory/")
async def create_new_item(item:InventoryItemCreate,db:Session=Depends(get_session)):
    db_product = create_inventory_item(session=db,item=item)
    return db_product

@app.get("/Inventory/")
def read_product(db:Session = Depends(get_session)):
    return get_inventory_item(session=db)


