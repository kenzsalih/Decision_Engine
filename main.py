import json
import sys
from engine.engine import run_engine


def main(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        result = run_engine(data)

        print("\n=== Surviving Options ===")
        for option in result["surviving"]:
            print("-", option.name)

        print("\n=== Normalized Utilities ===")
        for option_name, utilities in result["normalized"].items():
            print(f"{option_name}: {utilities}")

        print("\n=== Scores ===")
        for name, data in result["scored"].items():
            print(f"{name}: {data['final_score']}")

        print("\n=== Ranking ===")
        for item in result["ranked"]:
            print(
                f"Rank {item['rank']} - "
                f"{item['name']} "
                f"(Score: {item['final_score']})"
            )

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
        print("Usage: python main.py <input_json>")
        sys.exit(1)

    main(sys.argv[1])