import json
from pathlib import Path


class JSONStorage:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, filename, data):
        file_path = self.data_dir / filename

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self, filename):
        file_path = self.data_dir / filename

        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON data in {filename}")