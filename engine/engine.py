# engine/engine.py

from engine.validator import validate_input
from engine.input_parser import parse_input
from engine.constraint_filter import apply_constraints
from engine.normalization import normalize_all
from engine.scoring import score_options
from engine.ranking import rank_options

def run_engine(data: dict):
    """
    Full deterministic decision pipeline.
    """

    # 1. Validate raw input
    validate_input(data)

    # 2. Convert to dataclasses
    criteria, options = parse_input(data)

    # 3. Apply hard constraints (required criteria only)
    surviving_options = apply_constraints(criteria, options)

    if not surviving_options:
        return {
            "surviving": [],
            "normalized": {}
        }

    # 4. Normalize surviving options
    normalized = normalize_all(criteria, surviving_options)

    # 5. Score
    scored = score_options(criteria, surviving_options, normalized)

    # 6. Rank
    ranked = rank_options(scored)

    return {
        "surviving": surviving_options,
        "normalized": normalized,
        "scored": scored,
        "ranked": ranked
    }