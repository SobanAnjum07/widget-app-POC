from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models

router = APIRouter()


@router.get("/", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.code.asc()).all()


@router.post("/", response_model=schemas.ProductOut, status_code=201)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    exists = (
        db.query(models.Product)
        .filter(models.Product.code == payload.code)
        .first()
    )
    if exists:
        raise HTTPException(status_code=409, detail="Product code already exists")
    product = models.Product(code=payload.code, name=payload.name, price=payload.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
