from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.domain import Product, DeliveryChargeRule, Offer
from .offers import compute_offer_discount
from .delivery import compute_delivery_charge
from ..utils.calculations import round2

class BasketService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_total(self, basket_items: Dict[str, int]):
        if not basket_items:
            return 0.0, 0.0, 0.0, 0.0

        products = self.db.execute(select(Product)).scalars().all()
        catalogue = {p.code: p for p in products}
        rules = self.db.execute(select(DeliveryChargeRule).order_by(DeliveryChargeRule.min_total.asc())).scalars().all()
        offers = self.db.execute(select(Offer)).scalars().all()

        subtotal = 0.0
        for code, qty in basket_items.items():
            if code not in catalogue:
                raise ValueError(f"Unknown product code: {code}")
            subtotal += float(catalogue[code].price) * qty

        # Aggregate offers by product
        offers_by_product: dict[str, list[Offer]] = {}
        for offer in offers:
            if offer.product_code:
                offers_by_product.setdefault(offer.product_code, []).append(offer)

        discount = 0.0
        for code, qty in basket_items.items():
            if code in offers_by_product:
                unit_price = float(catalogue[code].price)
                for offer in offers_by_product[code]:
                    discount += compute_offer_discount(offer.type, qty, unit_price)

        order_total = subtotal - discount
        delivery = compute_delivery_charge(order_total, rules)
        total = order_total + delivery

        return round2(subtotal), round2(discount), round2(delivery), round2(total)
