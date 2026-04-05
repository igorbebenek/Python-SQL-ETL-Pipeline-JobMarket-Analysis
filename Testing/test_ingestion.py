import json
import os


def test_ingestion_results():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_dir, "..", "data", "raw", "raw_json_data_IT_only")

    # Check if the file exists
    assert os.path.exists(file_path), f"Error: Data file {file_path} not found"

    with open(file_path, 'r') as f:
        data = json.load(f)

        pl_count = len(data.get("pl", []))
        gb_count = len(data.get("gb", []))
        us_count = len(data.get("us", []))

        assert pl_count > 0, "Validation Failed: No job offers found for Poland"
        assert gb_count > 0, "Validation Failed: No job offers found for Great Britain"
        assert us_count > 0, "Validation Failed: No job offers found for USA"

        print(f"Passed: PL: {pl_count}, GB: {gb_count}, US: {us_count}")


if __name__ == "__main__":
    test_ingestion_results()