from engine.scoring import score_options
from models.dataclasses import Criterion, Option



def test_equal_weights_two_criteria():

    criteria = [
        Criterion(name="price", type="numeric", weight=None, required=False, goal="cost"),
        Criterion(name="quality", type="numeric", weight=None, required=False, goal="benefit"),
    ]

    options = [
        Option(name="A", values={"price": 100, "quality": 8}),
        Option(name="B", values={"price": 200, "quality": 6}),
    ]

    normalized = {
        "A": {"price": 1.0, "quality": 1.0},
        "B": {"price": 0.0, "quality": 0.0},
    }

    result = score_options(criteria, options, normalized)

    assert result["A"]["final_score"] == 1.0
    assert result["B"]["final_score"] == 0.0