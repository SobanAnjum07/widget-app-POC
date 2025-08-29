# def round2(value: float) -> float:
#     return round(float(value) + 1e-9, 2)

import math

def round2(value: float) -> float:
    return math.floor(float(value) * 100) / 100