from ..models.domain import OfferType


def compute_bogo_half_discount(quantity: int, unit_price: float) -> float:
    if quantity < 2:
        return 0.0
    discounted_items = quantity // 2
    return discounted_items * (unit_price / 2.0)


def compute_bogo_free_discount(quantity: int, unit_price: float) -> float:
    if quantity < 2:
        return 0.0
    free_items = quantity // 2
    return free_items * unit_price


def compute_offer_discount(offer_type: OfferType, quantity: int, unit_price: float) -> float:
    if offer_type == OfferType.BOGO_HALF:
        return compute_bogo_half_discount(quantity, unit_price)
    if offer_type == OfferType.BOGO_FREE:
        return compute_bogo_free_discount(quantity, unit_price)
    return 0.0
