from engine.engine import run_engine

def test_normalization_after_filter():
    data = {
        "criteria": [
            {
                "name": "score",
                "type": "numeric",
                "goal": "benefit",
                "required": True,
                "constraints": [
                    {"operator": ">=", "value": 80}
                ]
            },
            {
                "name": "dummy",
                "type": "numeric",
                "goal": "benefit",
                "weight": 1
            }
        ],
        "options": [
            {"name": "A", "values": {"score": 50, "dummy": 10}},
            {"name": "B", "values": {"score": 80, "dummy": 20}},
            {"name": "C", "values": {"score": 100, "dummy": 30}}
        ]
    }

    result = run_engine(data)

    # surviving scores: [80, 100]
    assert result["normalized"]["B"]["dummy"] == 0.0
    assert result["normalized"]["C"]["dummy"] == 1.0