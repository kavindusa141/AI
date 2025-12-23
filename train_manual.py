import os
import sys

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add this directory to the python path so we can find 'models'
sys.path.append(current_dir)

# If the script is accidentally inside 'data', look one level up
if current_dir.endswith("data"):
    sys.path.append(os.path.dirname(current_dir))

try:
    from models.nn_model import train_model
except ImportError as e:
    print("❌ Error: Could not find the 'models' folder.")
    print("   Make sure this script is in the main project folder.")
    print(f"   Details: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting manual training...")
    print(f"📂 Looking for data in: {os.path.join(current_dir, 'data', 'training_data.csv')}")
    
    model = train_model()
    
    if model:
        print("\n✅ SUCCESS: The AI has learned from your data!")
        print("🧠 The model is saved. You can now run 'train_cli.py' to see better results.")
    else:
        print("\n❌ FAILURE: Could not train.")
        print("   Check if 'data/training_data.csv' exists and is not empty.")