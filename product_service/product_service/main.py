from fastapi import FastAPI,HTTPException,Depends
from sqlmodel import Session
from product_service.db import create_db_and_tables,get_session
from product_service.schemas import ProductCreate, ProductRead
from product_service.crud import create_product,get_product_by_id,get_products
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

@app.post("/product/",response_model=ProductRead)
async def create_new_product(product:ProductCreate,db:Session=Depends(get_session)):
    db_product = create_product(session=db,product=product)
    return db_product

@app.get("/product/")
def read_product(db:Session = Depends(get_session)):
    return get_products(session=db)


