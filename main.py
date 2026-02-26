from engine.engine import run_engine

def main(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        result = run_engine(data)

        print("Surviving options:")
        for option in result["surviving"]:
            print("-", option["name"])

        print("\nNormalized numeric criteria:")
        for criterion, utilities in result["normalized"].items():
            print(f"{criterion}: {utilities}")

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