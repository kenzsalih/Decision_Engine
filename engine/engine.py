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
    criteria = data["criteria"]

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