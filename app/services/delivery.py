# from typing import List
# from ..models.domain import DeliveryChargeRule


# def compute_delivery_charge(order_total: float, rules: List[DeliveryChargeRule]) -> float:
#     if not rules:
#         return 0.0
#     applicable = [r for r in rules if float(r.min_total) <= order_total]
#     if applicable:
#         return float(sorted(applicable, key=lambda r: float(r.min_total))[-1].charge)
#     return float(sorted(rules, key=lambda r: float(r.charge))[-1].charge)

from typing import List
from ..models.domain import DeliveryChargeRule

def compute_delivery_charge(order_total: float, rules: List[DeliveryChargeRule]) -> float:
    if not rules:
        return 0.0

    # Find the highest min_total ≤ order_total
    applicable_rule = max(
        (r for r in rules if float(r.min_total) <= order_total),
        key=lambda r: float(r.min_total),
        default=None
    )

    if applicable_rule:
        return float(applicable_rule.charge)

    # Fallback: highest charge if no rule applies
    return float(max(rules, key=lambda r: float(r.charge)).charge)
