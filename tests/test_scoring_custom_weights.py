from models.dataclasses import Criterion, Option
from engine.scoring import score_options

def test_custom_weights():

    criteria = [
        Criterion(name="price", type="numeric", weight=2, required=False, goal="cost"),
        Criterion(name="quality", type="numeric", weight=1, required=False, goal="benefit"),
    ]

    options = [
        Option(name="A", values={"price": 100, "quality": 8}),
    ]

    normalized = {
        "A": {"price": 0.5, "quality": 1.0},
    }

    result = score_options(criteria, options, normalized)

    # weights normalized: price=2/3, quality=1/3
    expected = round((0.5 * (2/3)) + (1.0 * (1/3)), 6)

    assert result["A"]["final_score"] == expected