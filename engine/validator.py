def validate_input(data: dict):
    # ----------------------------
    # Top-level structure
    # ----------------------------
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object.")

    if "criteria" not in data or "options" not in data:
        raise ValueError("Input must contain 'criteria' and 'options'.")

    criteria = data["criteria"]
    options = data["options"]

    if not isinstance(criteria, list) or not isinstance(options, list):
        raise ValueError("'criteria' and 'options' must be lists.")

    if not criteria:
        raise ValueError("Criteria cannot be empty.")

    if not options:
        raise ValueError("Options cannot be empty.")

    # ----------------------------
    # Validate Criteria Definitions
    # ----------------------------
    allowed_types = ["numeric", "categorical", "boolean"]
    seen_names = set()

    for c in criteria:
        if "name" not in c or "type" not in c:
            raise ValueError("Each criterion must contain 'name' and 'type'.")

        name = c["name"]

        if name in seen_names:
            raise ValueError(f"Duplicate criterion name detected: '{name}'")

        seen_names.add(name)

        if c["type"] not in allowed_types:
            raise ValueError(f"Invalid criterion type: {c['type']}")

        # Required flag must be boolean if present
        if "required" in c and not isinstance(c["required"], bool):
            raise ValueError(f"'required' must be boolean for criterion '{name}'.")

        # Numeric-specific validation
        if c["type"] == "numeric":
            if "goal" not in c:
                raise ValueError(f"Numeric criterion '{name}' must define 'goal'.")

            if c["goal"] not in ["benefit", "cost"]:
                raise ValueError(
                    f"Numeric criterion '{name}' goal must be 'benefit' or 'cost'."
                )

        # Constraint structure validation
        if "constraints" in c:
            if not isinstance(c["constraints"], list):
                raise ValueError(f"'constraints' must be a list in '{name}'.")

            for constraint in c["constraints"]:
                if "operator" not in constraint or "value" not in constraint:
                    raise ValueError(
                        f"Each constraint in '{name}' must contain 'operator' and 'value'."
                    )

    # ----------------------------
    # Weight Policy Validation
    # ----------------------------
    non_required = [c for c in criteria if not c.get("required", False)]

    weights_defined = [c.get("weight") is not None for c in non_required]

    if any(weights_defined) and not all(weights_defined):
        raise ValueError("Partial weight configuration is not allowed.")

    for c in non_required:
        if c.get("weight") == 0:
            raise ValueError("Zero weights are not allowed.")

    for c in criteria:
        if c.get("required", False) and c.get("weight") is not None:
            raise ValueError(
                f"Required criterion '{c['name']}' cannot have a weight."
            )

    # Reject case where all criteria are required (nothing to score)
    if all(c.get("required", False) for c in criteria):
        raise ValueError("At least one non-required criterion is required for scoring.")

    # ----------------------------
    # Validate Options
    # ----------------------------
    criterion_lookup = {c["name"]: c for c in criteria}

    for option in options:
        if "name" not in option or "values" not in option:
            raise ValueError("Each option must contain 'name' and 'values'.")

        if not isinstance(option["values"], dict):
            raise ValueError(f"'values' must be an object in option '{option['name']}'.")

        for criterion_name, criterion in criterion_lookup.items():

            if criterion_name not in option["values"]:
                raise ValueError(
                    f"Option '{option['name']}' missing value for criterion '{criterion_name}'."
                )

            value = option["values"][criterion_name]
            ctype = criterion["type"]

            # Type enforcement
            if ctype == "numeric":
                if not isinstance(value, (int, float)):
                    raise ValueError(
                        f"Value for '{criterion_name}' in option '{option['name']}' must be numeric."
                    )

            elif ctype == "boolean":
                if not isinstance(value, bool):
                    raise ValueError(
                        f"Value for '{criterion_name}' in option '{option['name']}' must be boolean."
                    )

            elif ctype == "categorical":
                if not isinstance(value, str):
                    raise ValueError(
                        f"Value for '{criterion_name}' in option '{option['name']}' must be a string."
                    )

    # If we reach here, input is valid