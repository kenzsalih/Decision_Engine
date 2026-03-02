from engine.validator import validate_input
from engine.constraint_filter import apply_constraints
from engine.normalization import Normalizer
# later:
# from engine.scoring import score_options
# from engine.ranking import rank_options


def run_engine(data: dict):
    """
    Orchestrates full decision pipeline.
    """

    # 1. Validate
    validate_input(data)

    # 2. Apply constraints
    surviving = apply_constraints(data)

    if not surviving:
        return []

    # 3. Extract numeric criteria values
    
    

    normalized_results = {}

    for criterion in criteria:
        if criterion["type"] != "numeric":
            continue

        name = criterion["name"]
        ctype = criterion["goal"]  # benefit or cost

        values = [option["values"][name] for option in surviving]

        normalized = Normalizer.normalize_numeric(values, ctype)

        normalized_results[name] = normalized
        
    # Placeholder return for now
    return {
        "surviving": surviving,
        "normalized": normalized_results
    }


"""
Constraint filtering layer - eliminates options that violate hard constraints.
"""
from typing import List
from models.dataclasses import Criterion, Option


def apply_constraints(criteria: List[Criterion], options: List[Option]) -> List[Option]:
    """
    Filter options based on hard constraints.
    
    Args:
        criteria: List of Criterion objects
        options: List of Option objects
        
    Returns:
        List of Option objects that satisfy all constraints
    """
    surviving = []
    
    for option in options:
        if _satisfies_all_constraints(option, criteria):
            surviving.append(option)
    
    return surviving


def _satisfies_all_constraints(option: Option, criteria: List[Criterion]) -> bool:
    """
    Check if an option satisfies all constraints across all criteria.
    
    Args:
        option: Option object to check
        criteria: List of all Criterion objects
        
    Returns:
        True if option passes all constraints, False otherwise
    """
    for criterion in criteria:
        if not criterion.constraints:
            continue
            
        criterion_name = criterion.name
        
        # Missing value fails if criterion is required
        if criterion_name not in option.values:
            if criterion.required:
                return False
            continue
        
        value = option.values[criterion_name]
        
        # Check each constraint for this criterion
        for constraint in criterion.constraints:
            if not _check_constraint(value, constraint):
                return False
    
    return True


def _check_constraint(value: any, constraint: dict) -> bool:
    """
    Check if a value satisfies a single constraint.
    
    Args:
        value: The value to check
        constraint: Dictionary with 'type' and 'value' keys
        
    Returns:
        True if constraint is satisfied, False otherwise
    """
    constraint_type = constraint["type"]
    constraint_value = constraint["value"]
    
    if constraint_type == "min":
        return value >= constraint_value
    elif constraint_type == "max":
        return value <= constraint_value
    elif constraint_type == "equals":
        return value == constraint_value
    
    return True

