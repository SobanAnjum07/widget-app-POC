from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...dependencies import get_db_session
from ....models import schemas as sc
from ....services.basket import BasketService

router = APIRouter()


@router.post("/total", response_model=sc.BasketTotalResponse)
def total(payload: sc.BasketTotalRequest, db: Session = Depends(get_db_session)):
    basket_map: dict[str, int] = {}
    for item in payload.items:
        basket_map[item.product_code] = basket_map.get(item.product_code, 0) + item.quantity

    try:
        subtotal, discount, delivery, total_ = BasketService(db).calculate_total(basket_map)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return sc.BasketTotalResponse(
        subtotal=subtotal, discount=discount, delivery=delivery, total=total_
    )
