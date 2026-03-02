"""
Input parsing layer - converts raw JSON to internal dataclass models.
"""
from typing import Any, Dict, List, Tuple
from models.dataclasses import Criterion, Option


def parse_input(data: Dict[str, Any]) -> Tuple[List[Criterion], List[Option]]:
    """
    Convert raw JSON input into internal dataclass objects.
    """

    criteria = [
        Criterion(
            name=c["name"],
            type=c["type"],
            weight=c.get("weight"),
            required=c.get("required", False),
            goal=c.get("goal"),
            constraints=c.get("constraints", [])
        )
        for c in data["criteria"]
    ]

    options = [
        Option(
            name=o["name"],
            values=dict(o["values"])  # defensive copy
        )
        for o in data["options"]
    ]

    return criteria, options