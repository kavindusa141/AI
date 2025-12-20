import json


class Environment:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.packages = json.load(f)

        if not isinstance(self.packages, list):
            raise ValueError("Tour package data must be a list")

    def get_packages(self):
        # Return a copy to protect environment integrity
        return list(self.packages)
