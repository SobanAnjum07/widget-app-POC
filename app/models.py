from sqlalchemy import String, Numeric, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
import enum
from .db import Base


class OfferType(str, enum.Enum):
    BOGO_HALF = "BOGO_HALF"  # Buy one get second half price (by product_code)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))


class DeliveryChargeRule(Base):
    __tablename__ = "delivery_charge_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    min_total: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    charge: Mapped[float] = mapped_column(Numeric(10, 2))


class Offer(Base):
    __tablename__ = "offers"
    __table_args__ = (
        UniqueConstraint("type", "product_code", name="uq_offer_type_product"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[OfferType] = mapped_column(Enum(OfferType), index=True)
    product_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
