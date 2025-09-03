from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.schemas import ProductCreate, ProductOut
from ..models.domain import Product

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.code.asc()).all()


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    exists = (
        db.query(Product)
        .filter(Product.code == payload.code)
        .first()
    )
    if exists:
        raise HTTPException(status_code=409, detail="Product code already exists")
    product = Product(code=payload.code, name=payload.name, price=payload.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
