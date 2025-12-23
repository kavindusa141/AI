import json
import os

class Environment:
    def __init__(self, path):
        # 1. robust File Handling
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Critical Error: Data file not found at {path}")

        with open(path, "r", encoding="utf-8") as f:
            self.packages = json.load(f)

        # 2. Basic Type Check
        if not isinstance(self.packages, list):
            raise ValueError("❌ Tour package data must be a list")

        # 3. DATA VALIDATION (The "University Polish")
        # This checks if your new 'generate_data.py' features are actually present.
        if self.packages:
            first_pkg = self.packages[0]
            first_activity = first_pkg['activities'][0] if first_pkg.get('activities') else {}
            
            # Check for the Map Coordinates we added
            if "lat" not in first_activity:
                print("⚠️ WARNING: Loaded data seems to be the OLD version (No Map Coordinates).")
                print("   👉 Run 'python generate_data.py' to fix this.")
            
            # Check for Time Slots
            elif "preferred_time" not in first_activity:
                print("⚠️ WARNING: Loaded data is missing Time Slots (No Morning/Evening scheduling).")
                print("   👉 Run 'python generate_data.py' to fix this.")
                
            else:
                print(f"✅ Environment loaded {len(self.packages)} packages with Map & Time data.")

    def get_packages(self):
        # Return a shallow copy to protect environment integrity
        return list(self.packages)