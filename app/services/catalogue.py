from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import domain as dm
from ..core.exceptions import NotFoundError, ConflictError


class CatalogueService:
    def __init__(self, db: Session):
        self.db = db

    # Products CRUD
    def list_products(self):
        return self.db.execute(select(dm.Product).order_by(dm.Product.code.asc())).scalars().all()

    def get_product(self, code: str) -> dm.Product:
        product = self.db.execute(select(dm.Product).where(dm.Product.code == code)).scalar_one_or_none()
        if not product:
            raise NotFoundError("Product not found")
        return product

    def create_product(self, code: str, name: str, price: float) -> dm.Product:
        existing = self.db.execute(select(dm.Product).where(dm.Product.code == code)).scalar_one_or_none()
        if existing:
            raise ConflictError("Product code already exists")
        product = dm.Product(code=code, name=name, price=price)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, code: str, name: str | None, price: float | None) -> dm.Product:
        product = self.get_product(code)
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, code: str) -> None:
        product = self.get_product(code)
        self.db.delete(product)
        self.db.commit()

    # Delivery rules CRUD
    def list_delivery_rules(self):
        return self.db.execute(select(dm.DeliveryChargeRule).order_by(dm.DeliveryChargeRule.min_total.asc())).scalars().all()

    def create_delivery_rule(self, min_total: float, charge: float) -> dm.DeliveryChargeRule:
        rule = dm.DeliveryChargeRule(min_total=min_total, charge=charge)
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def update_delivery_rule(self, rule_id: int, min_total: float | None, charge: float | None) -> dm.DeliveryChargeRule:
        rule = self.db.get(dm.DeliveryChargeRule, rule_id)
        if not rule:
            raise NotFoundError("Delivery rule not found")
        if min_total is not None:
            rule.min_total = min_total
        if charge is not None:
            rule.charge = charge
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def delete_delivery_rule(self, rule_id: int) -> None:
        rule = self.db.get(dm.DeliveryChargeRule, rule_id)
        if not rule:
            raise NotFoundError("Delivery rule not found")
        self.db.delete(rule)
        self.db.commit()

    # Offers CRUD
    def list_offers(self):
        return self.db.execute(select(dm.Offer)).scalars().all()

    def create_offer(self, type_: dm.OfferType, product_code: str | None) -> dm.Offer:
        existing = self.db.execute(
            select(dm.Offer).where(dm.Offer.type == type_, dm.Offer.product_code == product_code)
        ).scalar_one_or_none()
        if existing:
            raise ConflictError("Offer already exists for product")
        offer = dm.Offer(type=type_, product_code=product_code)
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def update_offer(self, offer_id: int, type_: dm.OfferType | None, product_code: str | None) -> dm.Offer:
        offer = self.db.get(dm.Offer, offer_id)
        if not offer:
            raise NotFoundError("Offer not found")
        if type_ is not None:
            offer.type = type_
        if product_code is not None:
            offer.product_code = product_code
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def delete_offer(self, offer_id: int) -> None:
        offer = self.db.get(dm.Offer, offer_id)
        if not offer:
            raise NotFoundError("Offer not found")
        self.db.delete(offer)
        self.db.commit()
