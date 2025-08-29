```python
# Rules assumed to be in ascending min_total; find first that applies
# Example semantics: charge applies when order_total < next threshold; else 0
# We'll model rules as: rule applies if order_total < next_rule.min_total, else next
# To keep simple and flexible, storing rules as in problem statement:
# - min_total: 0, charge 4.95 (under 50)
# - min_total: 50, charge 2.95 (under 90)
# - min_total: 90, charge 0.0 (>=90)
# So we find the largest rule with min_total <= order_total and take its charge.

```