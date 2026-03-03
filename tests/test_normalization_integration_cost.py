from engine.engine import run_engine

def test_engine_normalization_cost():
    data = {
        "criteria": [
            {"name": "cost", "type": "numeric", "goal": "cost"}
        ],
        "options": [
            {"name": "A", "values": {"cost": 300}},
            {"name": "B", "values": {"cost": 200}},
            {"name": "C", "values": {"cost": 400}}
        ],
        "constraints": []
    }

    result = run_engine(data)

    assert result["normalized"]["A"]["cost"] == 0.5
    assert result["normalized"]["B"]["cost"] == 1.0
    assert result["normalized"]["C"]["cost"] == 0.0