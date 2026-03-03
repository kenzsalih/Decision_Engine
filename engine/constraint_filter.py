# engine/constraint_filter.py

from typing import List
from models.dataclasses import Criterion, Option


def apply_constraints(
    criteria: List[Criterion],
    options: List[Option]
) -> List[Option]:
    """
    Filter options based on hard constraints (required criteria only).
    """

    surviving = []

    for option in options:
        if _satisfies_all_constraints(option, criteria):
            surviving.append(option)

    return surviving


def _satisfies_all_constraints(
    option: Option,
    criteria: List[Criterion]
) -> bool:

    for criterion in criteria:

        # Only required criteria act as hard filters
        if not criterion.required:
            continue

        if not criterion.constraints:
            continue

        value = option.values.get(criterion.name)

        # Missing value fails if required
        if value is None:
            return False

        for constraint in criterion.constraints:
            if not _check_constraint(value, constraint):
                return False

    return True


def _check_constraint(value, constraint: dict) -> bool:

    # Old operator-based schema
    if "operator" in constraint:
        operator = constraint["operator"]
        target = constraint["value"]

        if operator == ">=":
            return value >= target
        elif operator == "<=":
            return value <= target
        elif operator == ">":
            return value > target
        elif operator == "<":
            return value < target
        elif operator == "==":
            return value == target
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    # New type-based schema (if ever used later)
    elif "type" in constraint:
        constraint_type = constraint["type"]
        target = constraint["value"]

        if constraint_type == "min":
            return value >= target
        elif constraint_type == "max":
            return value <= target
        elif constraint_type == "equals":
            return value == target
        else:
            raise ValueError(f"Unsupported constraint type: {constraint_type}")

    else:
        raise ValueError("Invalid constraint format.")