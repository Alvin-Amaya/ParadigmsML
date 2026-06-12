import os
import sys

# Add orchestrator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))

# Simulate the orchestrator normalization
base_path = os.path.dirname(os.path.abspath(__file__))

NORMALIZATION_PARAMS = {}

def load_normalization_params():
    """Load min/max normalization parameters from model files"""
    
    # Load imperative model params
    imperative_model_path = os.path.join(base_path, "modules", "imperative", "logistic_model.txt")
    print(f"Looking for model at: {imperative_model_path}")
    if os.path.exists(imperative_model_path):
        with open(imperative_model_path, 'r') as f:
            lines = f.readlines()
            print(f"File has {len(lines)} lines")
            for i, line in enumerate(lines):
                print(f"Line {i}: {line.strip()}")
            
            if len(lines) >= 4:
                min_values = list(map(float, lines[2].split()))
                max_values = list(map(float, lines[3].split()))
                NORMALIZATION_PARAMS["imperative"] = (min_values, max_values)
                print(f"\nLoaded normalization params:")
                print(f"  Min values: {min_values}")
                print(f"  Max values: {max_values}")
    
    return NORMALIZATION_PARAMS

def normalize(data, paradigm=None):
    """Normalize data using per-feature min/max normalization"""
    if paradigm and paradigm in NORMALIZATION_PARAMS:
        min_values, max_values = NORMALIZATION_PARAMS[paradigm]
        normalized = []
        for i, x in enumerate(data):
            if i < len(min_values) and i < len(max_values):
                min_val = min_values[i]
                max_val = max_values[i]
                if max_val - min_val > 0:
                    normalized.append((x - min_val) / (max_val - min_val))
                else:
                    normalized.append(0.0)
            else:
                normalized.append(x)
        return normalized
    else:
        # Fallback: global normalization if params not available
        min_val = min(data)
        max_val = max(data)
        if max_val - min_val == 0:
            return [0.0 for _ in data]
        return [(x - min_val) / (max_val - min_val) for x in data]

# Test
load_normalization_params()

test_data = [39, 1, 3, 120, 339, 0, 0, 170, 0, 0.0, 1]  # Corrected: added age (39)
print(f"\nOriginal data (with age): {test_data}")
normalized = normalize(test_data, "imperative")
print(f"Normalized data: {normalized}")

test_data2 = [40, 1, 2, 140, 289, 0, 0, 172, 0, 0.0, 1]
print(f"\nOriginal data (with age): {test_data2}")
normalized2 = normalize(test_data2, "imperative")
print(f"Normalized data: {normalized2}")

# Show that the normalization now produces values in [0, 1] range
print("\n--- Checking if all values are in [0, 1] range ---")
for i, val in enumerate(normalized):
    if val < 0 or val > 1:
        print(f"  Feature {i}: {val} - OUT OF RANGE")
    else:
        print(f"  Feature {i}: {val} - OK")
        
print("\nFor data 2:")
for i, val in enumerate(normalized2):
    if val < 0 or val > 1:
        print(f"  Feature {i}: {val} - OUT OF RANGE")
    else:
        print(f"  Feature {i}: {val} - OK")
