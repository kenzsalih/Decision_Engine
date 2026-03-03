from typing import Dict, List
from models.dataclasses import Criterion, Option, UtilityBreakdown


PRECISION = 6


def score_options(
    criteria: List[Criterion],
    options: List[Option],
    normalized_utilities: Dict[str, Dict[str, float]]
) -> Dict[str, Dict]:
    """
    Compute deterministic weighted-sum scores.

    Returns:
        {
            option_name: {
                "final_score": float,
                "breakdown": List[UtilityBreakdown]
            }
        }
    """

    # 1️⃣ Filter scoring criteria (exclude required)
    scoring_criteria = [
        c for c in criteria
        if not c.required
    ]

    if not scoring_criteria:
        return {}

    # 2️⃣ Extract weights
    weights = [c.weight for c in scoring_criteria]

    # 3️⃣ Determine weight mode
    if all(w is None for w in weights):
        normalized_weights = {
            c.name: 1.0 / len(scoring_criteria)
            for c in scoring_criteria
        }
    else:
        total_weight = sum(weights)
        normalized_weights = {
            c.name: c.weight / total_weight
            for c in scoring_criteria
        }

    results = {}

    # 4️⃣ Score each option
    for option in options:

        breakdown_list: List[UtilityBreakdown] = []
        final_score = 0.0

        for criterion in scoring_criteria:

            raw_value = option.values[criterion.name]
            utility = normalized_utilities[option.name][criterion.name]
            weight = normalized_weights[criterion.name]

            contribution = utility * weight

            breakdown = UtilityBreakdown(
                criterion=criterion.name,
                raw_value=raw_value,
                utility=utility,
                weight=weight,
                contribution=contribution
            )

            breakdown_list.append(breakdown)
            final_score += contribution

        final_score = round(final_score, PRECISION)

        results[option.name] = {
            "final_score": final_score,
            "breakdown": breakdown_list
        }

    return results