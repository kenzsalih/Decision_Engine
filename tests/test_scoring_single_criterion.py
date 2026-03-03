from models.dataclasses import Criterion, Option
from engine.scoring import score_options

def test_single_criterion():

    criteria = [
        Criterion(name="speed", type="numeric", weight=None, required=False, goal="benefit"),
    ]

    options = [
        Option(name="A", values={"speed": 10}),
    ]

    normalized = {
        "A": {"speed": 0.75},
    }

    result = score_options(criteria, options, normalized)

    assert result["A"]["final_score"] == 0.75