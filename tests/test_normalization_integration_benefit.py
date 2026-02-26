from engine.engine import run_engine


def test_engine_normalization_benefit():

    data = {
        "criteria": [
            {
                "name": "performance",
                "type": "numeric",
                "goal": "benefit"
            }
        ],
        "options": [
            {"name": "AWS", "values": {"performance": 80}},
            {"name": "Azure", "values": {"performance": 70}},
            {"name": "GCP", "values": {"performance": 90}}
        ],
        "constraints": []
    }

    result = run_engine(data)

    assert result["normalized"]["performance"] == [0.5, 0.0, 1.0]