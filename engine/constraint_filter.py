def apply_constraints(data: dict):
    criteria = data["criteria"]
    options = data["options"]

    surviving = []

    for option in options:
        eliminate = False

        for criterion in criteria:
            if not criterion.get("constraints"):
                continue

            value = option["values"].get(criterion["name"])

            for constraint in criterion["constraints"]:
                if constraint["operator"] == ">=":
                    if value < constraint["value"]:
                        eliminate = True
                elif constraint["operator"] == "<=":
                    if value > constraint["value"]:
                        eliminate = True
                elif constraint["operator"] == "==":
                    if value != constraint["value"]:
                        eliminate = True

        if not eliminate:
            surviving.append(option)

    return surviving