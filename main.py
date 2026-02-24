import json
import sys
from engine.validator import validate_input
from engine.constraint_filter import apply_constraints


def main(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    validate_input(data)

    surviving = apply_constraints(data)

    print("Surviving options after constraint filtering:")
    for option in surviving:
        print("-", option["name"])


if __name__ == "__main__":
    main(sys.argv[1])