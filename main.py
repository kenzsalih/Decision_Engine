import json
import sys
from engine.validator import validate_input
from engine.constraint_filter import apply_constraints


def main(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        validate_input(data)

        surviving = apply_constraints(data)

        print("Surviving options after constraint filtering:")
        for option in surviving:
            print("-", option["name"])

    except ValueError as e:
        print(f"Validation Error: {e}")
        sys.exit(1)

    except FileNotFoundError:
        print("Error: Input file not found.")
        sys.exit(1)

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_json_file>")
        sys.exit(1)

    main(sys.argv[1])