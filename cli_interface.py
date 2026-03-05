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

        print("\nAvailable Criteria:")
        for i, c in enumerate(data["criteria"], start=1):
            print(f"{i}. {c['name']}")

        selected = input(
            "\nEnter criteria numbers separated by comma (example: 1,3): "
        )

        selected_indexes = [int(x.strip()) - 1 for x in selected.split(",")]

        selected_criteria = [
            data["criteria"][i] for i in selected_indexes
        ]

        data["criteria"] = selected_criteria

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

    for i in range(num_criteria):
        print(f"\nCriterion {i+1}")

        name = input("Name: ")

        while True:
            goal = input("Goal (benefit/cost): ").strip().lower()

            if goal in ["benefit", "cost"]:
                break

            print("Invalid input. Please enter 'benefit' or 'cost'.")

        criterion = {
            "name": name,
            "type": "numeric",
            "goal": goal
        }

        if use_weights:
            weight = float(input("Weight: "))
            criterion["weight"] = weight

        criteria.append(criterion)

    print("\nEnter values for each option:")

    for option in options:
        print(f"\nOption: {option['name']}")

        for c in criteria:
            value = float(input(f"{c['name']}: "))
            option["values"][c["name"]] = value

    print("\nAll inputs collected.")
    print("Enter constraints (optional):")

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

        cname = criteria[idx]["name"]

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

        print(f"\nRank {item['rank']} - {name} (Score: {score})")

        breakdown = result["scored"][name]["breakdown"]

        print("\nCriterion        Value    Utility   Weight   Contribution")
        print("-----------------------------------------------------------")

        for row in breakdown:
            print(
                f"{row.criterion:<15}"
                f"{row.raw_value:<8}"
                f"{row.utility:<10.3f}"
                f"{row.weight:<9.3f}"
                f"{row.contribution:<10.3f}"
            )