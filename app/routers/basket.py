from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas
from ..services import PricingService

router = APIRouter()


@router.post("/total", response_model=schemas.BasketTotalResponse)
def calculate_total(payload: schemas.BasketTotalRequest, db: Session = Depends(get_db)):
    # Normalize items into a product_code -> quantity map
    basket_map: dict[str, int] = {}
    for item in payload.items:
        basket_map[item.product_code] = basket_map.get(item.product_code, 0) + item.quantity

    service = PricingService(db)
    try:
        subtotal, discount, delivery, total = service.calculate_total(basket_map)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return schemas.BasketTotalResponse(
        subtotal=subtotal, discount=discount, delivery=delivery, total=total
    )
