import os
import json

MATCH_DATA_FOLDER = "/Users/gavinschrader/whistleWatch/matchData"
OUTPUT_FILE = "refStats.json"

ref_stats = {}

# Loop through every JSON file inside matchData/
for filename in os.listdir(MATCH_DATA_FOLDER):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(MATCH_DATA_FOLDER, filename)
    
    with open(file_path, "r") as f:
        matches = json.load(f)

    # Each file contains an array of match objects
    for match in matches:
        referee = match.get("referee")
        if not referee:
            continue  # skip incomplete entries

        # Initialize referee totals if not created yet
        if referee not in ref_stats:
            ref_stats[referee] = {
                "referee": referee,
                "games": 0,
                "totalRedCard": 0.0,
                "totalYellowCards": 0.0,
                "totalFouls": 0.0,

                "homeFouls": 0.0,
                "homeRedCard": 0.0,
                "homeYellowCard": 0.0,

                "awayFouls": 0.0,
                "awayRedCard": 0.0,
                "awayYellowCard": 0.0
            }

        # Increment match count
        ref_stats[referee]["games"] += 1

        home = match["homeTeam"]
        away = match["awayTeam"]

        # HOME team contributions
        ref_stats[referee]["homeFouls"] += home.get("fkFoulLost", 0)
        ref_stats[referee]["homeRedCard"] += home.get("totalRedCard", 0)
        ref_stats[referee]["homeYellowCard"] += home.get("totalYellowCards", 0)

        # AWAY team contributions
        ref_stats[referee]["awayFouls"] += away.get("fkFoulLost", 0)
        ref_stats[referee]["awayRedCard"] += away.get("totalRedCard", 0)
        ref_stats[referee]["awayYellowCard"] += away.get("totalYellowCards", 0)

        # Totals (home + away)
        ref_stats[referee]["totalFouls"] += home.get("fkFoulLost", 0) + away.get("fkFoulLost", 0)
        ref_stats[referee]["totalRedCard"] += home.get("totalRedCard", 0) + away.get("totalRedCard", 0)
        ref_stats[referee]["totalYellowCards"] += home.get("totalYellowCards", 0) + away.get("totalYellowCards", 0)

# Save to output JSON
with open(OUTPUT_FILE, "w") as f:
    json.dump(list(ref_stats.values()), f, indent=4)

print(f"Referee stats created → {OUTPUT_FILE}")
