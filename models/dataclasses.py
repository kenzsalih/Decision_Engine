from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Criterion:
    name: str
    type: str  # numeric | categorical | boolean
    weight: Optional[float]
    required: bool
    benefit: Optional[bool] = None
    constraints: Optional[List[Dict[str, Any]]] = None


@dataclass
class Option:
    name: str
    values: Dict[str, Any]


@dataclass
class UtilityBreakdown:
    criterion: str
    raw_value: Any
    utility: float
    weight: float
    contribution: float