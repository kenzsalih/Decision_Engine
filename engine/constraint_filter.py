# engine/constraint_filter.py

from typing import List
from models.dataclasses import Criterion, Option


def apply_constraints(criteria: List[Criterion], options: List[Option]) -> List[Option]:
    """
    Filter options based on constraints defined on criteria.
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

        # Skip criteria that have no constraints
        if not criterion.constraints:
            continue

        value = option.values.get(criterion.name)

        # Missing value fails constraint check
        if value is None:
            return False

        for constraint in criterion.constraints:
            if not _check_constraint(value, constraint):
                return False

    return True


def _check_constraint(value, constraint: dict) -> bool:

    # Operator-based constraints
    if "operator" in constraint:
        operator = constraint["operator"]

        if operator == ">=":
            return value >= constraint["value"]

        elif operator == "<=":
            return value <= constraint["value"]

        elif operator == ">":
            return value > constraint["value"]

        elif operator == "<":
            return value < constraint["value"]

        elif operator == "==":
            return value == constraint["value"]

        elif operator == "between":
            return constraint["min"] <= value <= constraint["max"]

        else:
            raise ValueError(f"Unsupported operator: {operator}")

    # Alternative schema support (future)
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