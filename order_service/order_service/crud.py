from sqlmodel import Session,select
from product_service.models import Product
from product_service.schemas import ProductCreate,ProductRead
from typing import Optional

def get_product_by_id(session:Session,product_id:int)->Optional[Product]:
    statment = select(Product).where(Product.id == product_id)
    return session.exec(statment).first()

def create_product(session:Session, product:ProductCreate)->Product:
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def get_products(session:Session):
    statment = select(Product)
    return session.exec(statment).all()