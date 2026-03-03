from engine.engine import run_engine

def test_full_pipeline_with_constraints():

    data = {
        "criteria": [
            {
                "name": "safety",
                "type": "boolean",
                "required": True,
                "constraints": [
                    {"operator": "==", "value": True}
                ]
            },
            {
                "name": "performance",
                "type": "numeric",
                "goal": "benefit"
            }
        ],
        "options": [
            {"name": "A", "values": {"safety": True, "performance": 80}},
            {"name": "B", "values": {"safety": False, "performance": 100}},
            {"name": "C", "values": {"safety": True, "performance": 90}},
        ]
    }

    result = run_engine(data)

    ranked = result["ranked"]

    # B should be eliminated
    names = [r["name"] for r in ranked]

    assert "B" not in names
    assert ranked[0]["name"] == "C"