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

from typing import Dict, List
from models.dataclasses import Criterion, Option


def normalize_all(
    criteria: List[Criterion],
    options: List[Option]
) -> Dict[str, Dict[str, float]]:

    normalized_results = {
        option.name: {}
        for option in options
    }

    for criterion in criteria:

        # Required criteria are NOT scored
        if criterion.required:
            continue

        if criterion.type == "numeric":

            values = [
                option.values[criterion.name]
                for option in options
            ]

            normalized_values = Normalizer.normalize_numeric(
                values,
                criterion.goal
            )

            for i, option in enumerate(options):
                normalized_results[option.name][criterion.name] = normalized_values[i]

        elif criterion.type == "boolean":

            for option in options:
                raw = option.values[criterion.name]
                normalized_results[option.name][criterion.name] = 1.0 if raw else 0.0

        elif criterion.type == "categorical":

            raise NotImplementedError(
                f"Categorical normalization not implemented: {criterion.name}"
            )

    return normalized_results