from typing import List


"""
Normalization module for Decision Companion Engine.

Implements deterministic min-max normalization for numeric criteria.
Follows engine rules:

- Normalization happens AFTER constraint filtering.
- Computed only on surviving options.
- Benefit: (x - min) / (max - min)
- Cost:    (max - x) / (max - min)
- Edge case max == min -> utility = 1
- Fixed precision: 6 decimals
"""


class Normalizer:

    PRECISION = 6

    @staticmethod
    def normalize_numeric(values: List[float], criterion_type: str) -> List[float]:
        
        if not values:
            return []

        if criterion_type not in ("benefit", "cost"):
            raise ValueError("criterion_type must be 'benefit' or 'cost'")

        min_val = min(values)
        max_val = max(values)

        # Edge case: no variance
        if max_val == min_val:
            return [1.0] * len(values)

        normalized = []

        for v in values:
            if criterion_type == "benefit":
                utility = (v - min_val) / (max_val - min_val)
            else:  # cost
                utility = (max_val - v) / (max_val - min_val)

            normalized.append(round(utility, Normalizer.PRECISION))

        return normalized