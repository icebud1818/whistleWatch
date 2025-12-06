import os
import json

MATCH_DATA_FOLDER = "/Users/gavinschrader/whistleWatch/matchData"
OUTPUT_FILE = "allMatches.json"

all_matches = []

# Iterate through all files in the folder
for filename in os.listdir(MATCH_DATA_FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(MATCH_DATA_FOLDER, filename)
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                all_matches.extend(data)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {filename}")

# Save combined matches
with open(OUTPUT_FILE, "w") as f:
    json.dump(all_matches, f, indent=4)

print(f"Combined {len(all_matches)} matches into {OUTPUT_FILE}")
