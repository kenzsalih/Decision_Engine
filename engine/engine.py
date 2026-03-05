# engine/engine.py

from engine.validator import validate_input
from engine.input_parser import parse_input
from engine.constraint_filter import apply_constraints
from engine.normalization import normalize_all
from engine.scoring import score_options
from engine.ranking import rank_options

def run_engine(data: dict):

    validate_input(data)

    criteria, options = parse_input(data)

    constraints = data.get("constraints", [])

    # Attach CLI constraints to criteria objects
    for constraint in constraints:
        cname = constraint["criterion"]

        for c in criteria:
            if c.name == cname:
                if not hasattr(c, "constraints") or c.constraints is None:
                    c.constraints = []
                c.constraints.append(constraint)
                

    surviving_options = apply_constraints(criteria, options)

    if not surviving_options:
        return {
            "surviving": [],
            "normalized": {}
        }

    normalized = normalize_all(criteria, surviving_options)

    scored = score_options(criteria, surviving_options, normalized)

    ranked = rank_options(scored)

    return {
        "surviving": surviving_options,
        "normalized": normalized,
        "scored": scored,
        "ranked": ranked
    }