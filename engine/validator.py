def validate_input(data: dict):
    if "criteria" not in data or "options" not in data:
        raise ValueError("Input must contain 'criteria' and 'options'.")

    criteria = data["criteria"]
    options = data["options"]

    if not criteria or not options:
        raise ValueError("Criteria and options cannot be empty.")

    non_required = [c for c in criteria if not c.get("required", False)]

    weights_defined = [c.get("weight") is not None for c in non_required]

    if any(weights_defined) and not all(weights_defined):
        raise ValueError("Partial weight configuration is not allowed.")

    for c in non_required:
        if c.get("weight") == 0:
            raise ValueError("Zero weights are not allowed.")

    for c in criteria:
        if c["type"] not in ["numeric", "categorical", "boolean"]:
            raise ValueError(f"Invalid criterion type: {c['type']}")