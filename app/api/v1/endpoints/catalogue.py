from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...dependencies import get_db_session
from ....services.catalogue import CatalogueService
from ....models.schemas import ProductCreate, ProductOut, ProductUpdate, DeliveryRuleCreate, DeliveryRuleOut, DeliveryRuleUpdate, OfferCreate, OfferOut, OfferUpdate
from ....core.exceptions import NotFoundError, ConflictError

router = APIRouter()


# Products
@router.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db_session)):
    return CatalogueService(db).list_products()


@router.get("/products/{code}", response_model=ProductOut)
def get_product(code: str, db: Session = Depends(get_db_session)):
    try:
        return CatalogueService(db).get_product(code)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db_session)):
    try:
        return CatalogueService(db).create_product(payload.code, payload.name, payload.price)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/products/{code}", response_model=ProductOut)
@router.patch("/products/{code}", response_model=ProductOut)
def update_product(code: str, payload: ProductUpdate, db: Session = Depends(get_db_session)):
    try:
        return CatalogueService(db).update_product(code, payload.name, payload.price)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/products/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(code: str, db: Session = Depends(get_db_session)):
    try:
        CatalogueService(db).delete_product(code)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Delivery rules
@router.get("/delivery-rules", response_model=list[DeliveryRuleOut])
def list_delivery_rules(db: Session = Depends(get_db_session)):
    return CatalogueService(db).list_delivery_rules()


@router.post("/delivery-rules", response_model=DeliveryRuleOut, status_code=status.HTTP_201_CREATED)
def create_delivery_rule(payload: DeliveryRuleCreate, db: Session = Depends(get_db_session)):
    return CatalogueService(db).create_delivery_rule(payload.min_total, payload.charge)


@router.put("/delivery-rules/{rule_id}", response_model=DeliveryRuleOut)
@router.patch("/delivery-rules/{rule_id}", response_model=DeliveryRuleOut)
def update_delivery_rule(rule_id: int, payload: DeliveryRuleUpdate, db: Session = Depends(get_db_session)):
    try:
        return CatalogueService(db).update_delivery_rule(rule_id, payload.min_total, payload.charge)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delivery-rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery_rule(rule_id: int, db: Session = Depends(get_db_session)):
    try:
        CatalogueService(db).delete_delivery_rule(rule_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Offers
@router.get("/offers", response_model=list[OfferOut])
def list_offers(db: Session = Depends(get_db_session)):
    return CatalogueService(db).list_offers()


@router.post("/offers", response_model=OfferOut, status_code=status.HTTP_201_CREATED)
def create_offer(payload: OfferCreate, db: Session = Depends(get_db_session)):
    try:
        return CatalogueService(db).create_offer(payload.type, payload.product_code)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/offers/{offer_id}", response_model=OfferOut)
@router.patch("/offers/{offer_id}", response_model=OfferOut)
def update_offer(offer_id: int, payload: OfferUpdate, db: Session = Depends(get_db_session)):
    try:
        return CatalogueService(db).update_offer(offer_id, payload.type, payload.product_code)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/offers/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(offer_id: int, db: Session = Depends(get_db_session)):
    try:
        CatalogueService(db).delete_offer(offer_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
