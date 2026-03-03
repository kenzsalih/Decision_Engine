from models.dataclasses import Criterion, Option
from engine.scoring import score_options

def test_required_excluded_from_scoring():

    criteria = [
        Criterion(name="safety", type="boolean", weight=None, required=True),
        Criterion(name="price", type="numeric", weight=None, required=False, goal="cost"),
    ]

    options = [
        Option(name="A", values={"safety": True, "price": 100}),
    ]

    normalized = {
        "A": {"price": 0.8},
    }

    result = score_options(criteria, options, normalized)

    # Only one scoring criterion → weight = 1
    assert result["A"]["final_score"] == 0.8