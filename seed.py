from app.db import Base, engine, SessionLocal
from app.models import domain as dm


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Products
        defaults = [
            {"code": "R01", "name": "Red Widget", "price": 32.95},
            {"code": "G01", "name": "Green Widget", "price": 24.95},
            {"code": "B01", "name": "Blue Widget", "price": 7.95},
        ]
        for p in defaults:
            if not db.query(dm.Product).filter(dm.Product.code == p["code"]).first():
                db.add(dm.Product(**p))
        db.commit()

        # Delivery rules
        rules = [
            {"min_total": 0.00, "charge": 4.95},   # under $50
            {"min_total": 50.00, "charge": 2.95},  # under $90
            {"min_total": 90.00, "charge": 0.00},  # $90 or more
        ]
        for r in rules:
            exists = (
                db.query(dm.DeliveryChargeRule)
                .filter(dm.DeliveryChargeRule.min_total == r["min_total"])
                .first()
            )
            if not exists:
                db.add(dm.DeliveryChargeRule(**r))
        db.commit()

        # Offers: Buy one red widget, get second half price
        if not (
            db.query(dm.Offer)
            .filter(
                dm.Offer.type == dm.OfferType.BOGO_HALF,
                dm.Offer.product_code == "R01",
            )
            .first()
        ):
            db.add(dm.Offer(type=dm.OfferType.BOGO_HALF, product_code="R01"))
        db.commit()

        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
