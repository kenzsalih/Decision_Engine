import json
from engine.engine import run_engine


def start_cli():
    print("\n=== Decision Companion Engine ===")
    print("Deterministic MCDA decision system")

    while True:
        print("\nSelect mode:")
        print("1. Run cloud provider example")
        print("2. Create your own decision")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            run_cloud_example()

        elif choice == "2":
            run_custom_decision()

        elif choice == "3":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


def run_cloud_example():
    try:
        with open("sample_inputs/cloud_provider_selection.json", "r") as f:
            data = json.load(f)

        print("\nCloud Provider Selection Example")

        all_criteria = data["criteria"]

        print("\nAvailable Criteria:")
        for i, c in enumerate(all_criteria, start=1):
            print(f"{i}. {c['name']}")

        selected = input(
            "\nEnter criteria numbers that you are interested in, separated by comma (example: 1,3): "
        )

        selected_indexes = []
        seen = set()

        for x in selected.split(","):
            try:
                idx = int(x.strip()) - 1
                if 0 <= idx < len(all_criteria) and idx not in seen:
                    selected_indexes.append(idx)
                    seen.add(idx)
                else:
                    print(f"Ignoring invalid criterion number: {x}")
            except ValueError:
                print(f"Ignoring invalid input: {x}")

        selected_indexes = list(set(selected_indexes))
        selected_criteria = []

        use_weights = input(
            "Do you want to assign weights? (y/n): "
        ).strip().lower() == "y"

        weights = []

        for idx in selected_indexes:
            base = all_criteria[idx]

            criterion = {
                "name": base["name"],
                "type": base["type"],
                "goal": base.get("goal")
            }

            if use_weights:
                weight = float(input(f"Weight for {base['name']}: "))
                weights.append(weight)
                criterion["weight"] = weight

            selected_criteria.append(criterion)

        if use_weights:
            total = sum(weights)
            if abs(total - 1.0) > 1e-6:
                print(f"\nWarning: weights sum to {total:.3f}. They will be normalized by the engine.")

        constraints = add_constraints(selected_criteria)

        data["criteria"] = selected_criteria
        data["constraints"] = constraints

        result = run_engine(data)

        display_results(result)

    except Exception as e:
        print(f"Error: {e}")


def run_custom_decision():
    topic = input("\nEnter decision topic: ")

    num_options = int(input("Number of options: "))
    options = []

    for i in range(num_options):
        name = input(f"Option {i+1} name: ")
        options.append({"name": name, "values": {}})

    num_criteria = int(input("\nNumber of criteria: "))

    use_weights = input(
        "Do you want to assign weights? (y/n): "
    ).strip().lower() == "y"

    criteria = []
    weights = []

    for i in range(num_criteria):
        print(f"\nCriterion {i+1}")

        name = input("Name: ")

        while True:
            ctype = input("Type (numeric/boolean): ").strip().lower()

            if ctype in ["numeric", "boolean"]:
                break

            print("Invalid input. Please enter 'numeric' or 'boolean'.")

        criterion = {
            "name": name,
            "type": ctype
        }

        if ctype == "numeric":
            while True:
                goal = input("Goal (benefit/cost): ").strip().lower()

                if goal in ["benefit", "cost"]:
                    break

                print("Invalid input. Please enter 'benefit' or 'cost'.")

            criterion["goal"] = goal

        if use_weights:
            weight = float(input("Weight: "))
            weights.append(weight)
            criterion["weight"] = weight

        criteria.append(criterion)

    if use_weights:
        total = sum(weights)
        if abs(total - 1.0) > 1e-6:
            print("\nWarning: weights do not sum to 1. They will be normalized by the engine.")

    print("\nEnter values for each option:")

    for option in options:
        print(f"\nOption: {option['name']}")

        for c in criteria:
            if c["type"] == "boolean":
                while True:
                    value_input = input(f"{c['name']} (true/false): ").strip().lower()
                    if value_input in ["true", "false"]:
                        value = value_input == "true"
                        break
                    print("Invalid input. Please enter 'true' or 'false'.")
            else:
                value = float(input(f"{c['name']}: "))
            
            option["values"][c["name"]] = value

    print("\nAll inputs collected.")

    constraints = add_constraints(criteria)

    data = {
        "criteria": criteria,
        "options": options,
        "constraints": constraints
    }

    try:
        result = run_engine(data)
        display_results(result)

    except Exception as e:
        print(f"Error: {e}")


def add_constraints(criteria):
    constraints = []

    print("\nDo you want to add constraints? (y/n)")
    use_constraints = input().strip().lower()

    if use_constraints != "y":
        return constraints

    while True:
        print("\nSelect criterion to constrain:")

        for i, c in enumerate(criteria, start=1):
            print(f"{i}. {c['name']}")

        while True:
            try:
                idx = int(input("Enter number: ")) - 1
                if 0 <= idx < len(criteria):
                    break
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a number.")

        c = criteria[idx]
        cname = c["name"]
        ctype = c["type"]

        if ctype == "boolean":

            print("\nBoolean constraint:")
            print("1. must be True")
            print("2. must be False")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                constraints.append({
                    "criterion": cname,
                    "operator": "==",
                    "value": True
                })

            elif choice == "2":
                constraints.append({
                    "criterion": cname,
                    "operator": "==",
                    "value": False
                })

            else:
                print("Invalid choice.")
                continue

        else:

            print("\nConstraint type:")
            print("1. >")
            print("2. <")
            print("3. >=")
            print("4. <=")
            print("5. between")

            ctype = input("Enter choice: ").strip()

            if ctype == "1":
                value = float(input("Enter value: "))
                constraints.append({"criterion": cname, "operator": ">", "value": value})

            elif ctype == "2":
                value = float(input("Enter value: "))
                constraints.append({"criterion": cname, "operator": "<", "value": value})

            elif ctype == "3":
                value = float(input("Enter value: "))
                constraints.append({"criterion": cname, "operator": ">=", "value": value})

            elif ctype == "4":
                value = float(input("Enter value: "))
                constraints.append({"criterion": cname, "operator": "<=", "value": value})

            elif ctype == "5":
                min_v = float(input("Minimum value: "))
                max_v = float(input("Maximum value: "))

                constraints.append({
                    "criterion": cname,
                    "operator": "between",
                    "min": min_v,
                    "max": max_v
                })

            else:
                print("Invalid choice.")

        more = input("\nAdd another constraint? (y/n): ").strip().lower()

        if more != "y":
            break

    return constraints


def display_results(result):

    print("\n=== Surviving Options ===")
    for option in result["surviving"]:
        print("-", option.name)

    if not result["surviving"]:
        print("\nNo options satisfy the constraints.")
        return

    print("\n=== Ranking ===")

    for item in result["ranked"]:
        name = item["name"]
        score = item["final_score"]

        print(f"\nRank {item['rank']} - {name} (Score: {score:.6f})")

        breakdown = result["scored"][name]["breakdown"]

        print("\nCriterion                 Value    Utility   Weight   Contribution")
        print("--------------------------------------------------------------------")

        for row in breakdown:

            value = row.raw_value
            if isinstance(value, bool):
                value = str(value)

            print(
                f"{row.criterion:<25}"
                f"{value:<10}"
                f"{row.utility:<12.3f}"
                f"{row.weight:<11.3f}"
                f"{row.contribution:<12.3f}"
            )

    print("\nDecision analysis complete.")