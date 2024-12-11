from fastapi import FastAPI,HTTPException,Depends
from sqlmodel import Session
from product_service.db import create_db_and_tables,get_session
from product_service.schemas import ProductCreate, ProductRead
from product_service.crud import create_product,get_product_by_id,get_products
from typing import Optional 
from contextlib import asynccontextmanager
from product_service.kafka.producer import get_kafka_producer,KafkaProducer
from product_service.kafka.consumer import run_consumer
from asyncio import create_task

from product_service.kafka import _pb2
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    consumer_task = create_task(run_consumer())
    try:
        yield
    finally:
        consumer_task.cancel()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/product/",response_model=ProductRead)
async def create_new_product(product:ProductCreate,db:Session=Depends(get_session),producer:KafkaProducer=Depends(get_kafka_producer)):
    db_product = create_product(session=db,product=product)
    product_registered = _pb2.ProductRegistered(
        product_id = db_product.id,
        name = db_product.name,
        price = db_product.price
    )
    await producer.send("product-registered",product_registered)
    return db_product

@app.get("/product/")
def read_product(db:Session = Depends(get_session)):
    return get_products(session=db)


