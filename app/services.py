from typing import Dict, List
from sqlalchemy.orm import Session
from .models import Product, DeliveryChargeRule, Offer, OfferType
from .utils.calculations import round2


class PricingService:
    def __init__(self, db: Session):
        self.db = db

    def _get_catalogue(self) -> Dict[str, Product]:
        products = self.db.query(Product).all()
        return {p.code: p for p in products}

    def _get_delivery_rules(self) -> List[DeliveryChargeRule]:
        return (
            self.db.query(DeliveryChargeRule)
            .order_by(DeliveryChargeRule.min_total.asc())
            .all()
        )

    def _get_offers(self) -> List[Offer]:
        return self.db.query(Offer).all()

    def calculate_total(self, basket_items: Dict[str, int]):
        if not basket_items:
            return 0.0, 0.0, 0.0, 0.0

        catalogue = self._get_catalogue()
        delivery_rules = self._get_delivery_rules()
        offers = self._get_offers()

        subtotal = 0.0
        for code, qty in basket_items.items():
            if code not in catalogue:
                raise ValueError(f"Unknown product code: {code}")
            subtotal += float(catalogue[code].price) * qty

        discount = 0.0
        # Apply offers - currently only BOGO_HALF per product
        for offer in offers:
            if offer.type == OfferType.BOGO_HALF and offer.product_code:
                code = offer.product_code
                if code in basket_items:
                    qty = basket_items[code]
                    if qty >= 2:
                        price = float(catalogue[code].price)
                        discounted_items = qty // 2
                        discount += discounted_items * (price / 2)

        order_total = subtotal - discount

        delivery = 0.0
        
        applicable = [r for r in delivery_rules if float(r.min_total) <= order_total]
        if applicable:
            delivery = float(sorted(applicable, key=lambda r: float(r.min_total))[-1].charge)
        else:
            # If misconfigured, default to highest charge among rules
            if delivery_rules:
                delivery = float(sorted(delivery_rules, key=lambda r: float(r.charge))[-1].charge)

        total = order_total + delivery
        return round2(subtotal), round2(discount), round2(delivery), round2(total)
