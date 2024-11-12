from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from order_service import schemas, crud
from order_service.db import create_db_and_tables, get_session
from typing import List
from contextlib import asynccontextmanager
import asyncio

from order_service.schemas import OrderCreate, OrderUpdate, OrderItemUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        yield
    finally:
        pass

app: FastAPI = FastAPI(lifespan=lifespan)

@app.post("/orders/", response_model=schemas.OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_session)):
    created_order = crud.create_order(db, order)
    return created_order


@app.get("/order", response_model=List[schemas.OrderList])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_orders(db, skip, limit)

@app.get("/order/{order_id}", response_model=schemas.OrderDetail)
def get_order_by_id(order_id: int, db: Session = Depends(get_session)):
    return crud.get_order_by_id(db, order_id)

@app.put("/order/{order_id}", response_model=schemas.OrderResponse)
async def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_session)):
    updated_order = crud.update_order(db, order_id, order)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/order/{order_id}", response_model=schemas.OrderResponse)
async def delete_order(order_id: int, db: Session = Depends(get_session)):
    deleted_order = crud.delete_order(db, order_id)
    if deleted_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order

@app.get("/order", response_model=List[schemas.OrderList])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_orders(db, skip, limit)

@app.get("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
def get_order_item_by_id(order_id: int, item_id: int, db: Session = Depends(get_session)):
    return crud.get_order_item_by_id(db, order_id, item_id)

@app.put("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
async def update_order_item(order_id: int, item_id: int, item: OrderItemUpdate, db: Session = Depends(get_session)):
    updated_item = crud.update_order_item(db, order_id, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    return updated_item

@app.delete("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
async def delete_order_item(order_id: int, item_id: int, db: Session = Depends(get_session)):
    deleted_item = crud.delete_order_item(db, order_id, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    return deleted_item