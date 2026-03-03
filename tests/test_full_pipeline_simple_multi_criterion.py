from engine.engine import run_engine


def test_full_pipeline_basic_ranking():

    data = {
        "criteria": [
            {
                "name": "price",
                "type": "numeric",
                "goal": "cost",
                "weight": 2
            },
            {
                "name": "quality",
                "type": "numeric",
                "goal": "benefit",
                "weight": 1
            }
        ],
        "options": [
            {"name": "A", "values": {"price": 100, "quality": 8}},
            {"name": "B", "values": {"price": 200, "quality": 9}},
            {"name": "C", "values": {"price": 150, "quality": 7}},
        ]
    }

    result = run_engine(data)

    ranked = result["ranked"]

    assert ranked[0]["rank"] == 1
    assert ranked[0]["name"] == "A"