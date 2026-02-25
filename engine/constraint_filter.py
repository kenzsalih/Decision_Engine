# constraint_filter.py

from typing import List, Dict, Any

EPSILON = 1e-6


SUPPORTED_OPERATORS = {">=", "<=", ">", "<", "=="}


def _compare(value: Any, operator: str, target: Any) -> bool:
    """
    Returns True if constraint is satisfied.
    Uses tolerance for numeric comparisons.
    """

    if operator not in SUPPORTED_OPERATORS:
        raise ValueError(f"Unsupported constraint operator: {operator}")

    # Numeric comparison with tolerance
    if isinstance(value, (int, float)) and isinstance(target, (int, float)):
        if operator == ">=":
            return value > target - EPSILON or abs(value - target) <= EPSILON
        elif operator == "<=":
            return value < target + EPSILON or abs(value - target) <= EPSILON
        elif operator == ">":
            return value > target + EPSILON
        elif operator == "<":
            return value < target - EPSILON
        elif operator == "==":
            return abs(value - target) <= EPSILON

    # Non-numeric (categorical / boolean) comparison
    if operator == "==":
        return value == target

    # Non-numeric values cannot use <, >, <=, >=
    raise TypeError(
        f"Operator '{operator}' not supported for non-numeric values."
    )


def apply_constraints(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filters options based on required criteria constraints.
    Returns list of surviving options.
    """

    criteria = data["criteria"]
    options = data["options"]

    surviving = []

    for option in options:
        eliminate = False

        for criterion in criteria:
            # Only required criteria act as hard constraints
            if not criterion.get("required", False):
                continue

            constraints = criterion.get("constraints")
            if not constraints:
                continue

            criterion_name = criterion["name"]
            value = option["values"].get(criterion_name)

            for constraint in constraints:
                operator = constraint["operator"]
                target = constraint["value"]

                if not _compare(value, operator, target):
                    eliminate = True
                    break  # AND logic within criterion

            if eliminate:
                break  # AND logic across required criteria

        if not eliminate:
            surviving.append(option)

    return surviving