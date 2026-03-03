from engine.engine import run_engine

def test_full_pipeline_tie_and_lexicographic():

    data = {
        "criteria": [
            {
                "name": "score",
                "type": "numeric",
                "goal": "benefit"
            }
        ],
        "options": [
            {"name": "beta", "values": {"score": 100}},
            {"name": "Alpha", "values": {"score": 100}},
        ]
    }

    result = run_engine(data)

    ranked = result["ranked"]

    # Same score → tie rank
    assert ranked[0]["rank"] == 1
    assert ranked[1]["rank"] == 1

    # Lexicographic ascending (case-insensitive)
    assert ranked[0]["name"] == "Alpha"
    assert ranked[1]["name"] == "beta"