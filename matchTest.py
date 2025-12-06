import requests

headers = {
    "Origin": "https://www.premierleague.com",
    "Referer": "https://www.premierleague.com/",
    "User-Agent": "Mozilla/5.0"
}

season = 2024
competition_id = 8  # Premier League
total_matchweeks = 38

all_match_ids = []

for matchweek in range(1, total_matchweeks + 1):
    url = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/competitions/{competition_id}/seasons/{season}/matchweeks/{matchweek}/matches"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        matches = data.get("data", [])
        match_ids = [match["matchId"] for match in matches]
        all_match_ids.extend(match_ids)
        print(f"Matchweek {matchweek} IDs: {match_ids}")
    else:
        print(f"Failed to fetch matchweek {matchweek}. Status code: {response.status_code}")

print("\nAll match IDs in the season:")
print(all_match_ids)
