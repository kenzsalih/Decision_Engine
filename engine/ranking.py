# engine/ranking.py

from typing import Dict, List

TOLERANCE = 1e-6


def rank_options(scored: Dict[str, Dict]) -> List[Dict]:
    """
    Rank options using dense ranking.

    Returns:
        [
            {
                "name": option_name,
                "rank": int,
                "final_score": float,
                "breakdown": [...]
            }
        ]
    """

    if not scored:
        return []

    # Convert to sortable list
    items = [
        {
            "name": name,
            "final_score": data["final_score"],
            "breakdown": data["breakdown"]
        }
        for name, data in scored.items()
    ]

    # Sort:
    # 1. final_score descending
    # 2. name ascending (case-insensitive)
    items.sort(
        key=lambda x: (-x["final_score"], x["name"].lower())
    )

    ranked_results = []

    current_rank = 1
    previous_score = None

    for index, item in enumerate(items):

        if previous_score is None:
            rank = current_rank
        else:
            if abs(item["final_score"] - previous_score) <= TOLERANCE:
                rank = current_rank
            else:
                current_rank += 1
                rank = current_rank

        ranked_results.append({
            "name": item["name"],
            "rank": rank,
            "final_score": item["final_score"],
            "breakdown": item["breakdown"]
        })

        previous_score = item["final_score"]

    return ranked_results