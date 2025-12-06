import requests
import json

# Team ID → Name mapping
team_mapping = {
    3: "Arsenal",
    7: "Aston Villa",
    91: "Bournemouth",
    94: "Brentford",
    36: "Brighton and Hove Albion",
    90: "Burnley",
    8: "Chelsea",
    31: "Crystal Palace",
    11: "Everton",
    54: "Fulham",
    2: "Leeds United",
    14: "Liverpool",
    43: "Manchester City",
    1: "Manchester United",
    4: "Newcastle United",
    17: "Nottingham Forest",
    56: "Sunderland",
    6: "Tottenham Hotspur",
    21: "West Ham United",
    39: "Wolverhampton Wanderers",
    13: "Leicester City",
    35: "West Bromwich Albion",
    49: "Sheffield United",
    45: "Norwich City",
    57: "Watford",
    20: "Southampton",
    102: "Luton Town",
    40: "Ipswich Town"
}

headers = {
    "Origin": "https://www.premierleague.com",
    "Referer": "https://www.premierleague.com/",
    "User-Agent": "Mozilla/5.0"
}

competition_id = 8
season = 2020  # change to current season if needed
total_matchweeks = 38  # only matchweeks that have occurred

# Step 1: Collect all match IDs so far
match_ids = []

for matchweek in range(1, total_matchweeks + 1):
    url = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/competitions/{competition_id}/seasons/{season}/matchweeks/{matchweek}/matches"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        matches = data.get("data", [])
        match_ids.extend([match["matchId"] for match in matches])
        print(f"Matchweek {matchweek}: {len(matches)} matches found.")
    else:
        print(f"Failed to fetch matchweek {matchweek}. Status code: {response.status_code}")

print(f"\nTotal matches found: {len(match_ids)}")

# Step 2: Fetch stats and referee info for each match
all_matches = []

for match_id in match_ids:
    url_stats = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v3/matches/{match_id}/stats"
    url_officials = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/matches/{match_id}/officials"

    # Stats
    response = requests.get(url_stats, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get stats for match {match_id}")
        continue
    data = response.json()

    # Officials
    refResponse = requests.get(url_officials, headers=headers)
    if refResponse.status_code != 200:
        print(f"Failed to get officials for match {match_id}")
        continue
    refData = refResponse.json()

    # Extract home and away
    home = next(item for item in data if item["side"] == "Home")
    away = next(item for item in data if item["side"] == "Away")

    # Extract main referee safely
    officials_list = refData.get("officials") or refData.get("matchOfficials") or []
    referee_entry = next((item for item in officials_list if item["type"] == "Referee"), None)
    referee_name = referee_entry["official"]["name"] if referee_entry else "Unknown"

    # Get goals safely
    home_goals = home["stats"].get("goals", 0)
    away_goals = away["stats"].get("goals", 0)

    # Determine results
    if home_goals > away_goals:
        home_result = "win"
        away_result = "loss"
    elif home_goals < away_goals:
        home_result = "loss"
        away_result = "win"
    else:
        home_result = away_result = "draw"

# Build match object with team names and result
    match_obj = {
    "matchId": match_id,
    "referee": referee_name,
    "homeTeam": {
        "teamId": home["teamId"],
        "teamName": team_mapping.get(int(home["teamId"]), "Unknown"),
        "goals": home_goals,
        "totalRedCard": home["stats"].get("totalRedCard", 0),
        "totalYellowCards": home["stats"].get("totalYelCard", 0),
        "fkFoulLost": home["stats"].get("fkFoulLost", 0),
        "result": home_result
    },
    "awayTeam": {
        "teamId": away["teamId"],
        "teamName": team_mapping.get(int(away["teamId"]), "Unknown"),
        "goals": away_goals,
        "totalRedCard": away["stats"].get("totalRedCard", 0),
        "totalYellowCards": away["stats"].get("totalYelCard", 0),
        "fkFoulLost": away["stats"].get("fkFoulLost", 0),
        "result": away_result
    }
}


    all_matches.append(match_obj)
    print(f"Processed match {match_id}")

# Step 3: Save to JSON
with open("2020-2021_data.json", "w") as f:
    json.dump(all_matches, f, indent=4)

print("\nCustom JSON for all matches created successfully!")
