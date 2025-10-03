import pandas as pd

def calculate_fantasy_points(row):
    points_dict = {
        'FGM': 2,
        'FGA': -1,
        'FTM': 1,
        'FTA': -1,
        '3PM': 2,
        '3PA': -1,
        'OREB': 1,
        'DREB': 2,
        'AST': 3,
        'STL': 4,
        'BLK': 4,
        'TO': -2,
        'PTS': 1,
        'didWin': 1  # we skip this for season totals
    }

    fantasy_points = 0
    for stat, weight in points_dict.items():
        if stat in row and pd.notna(row[stat]):
            try:
                fantasy_points += weight * int(row[stat])
            except ValueError:
                fantasy_points += weight * float(row[stat])
    return fantasy_points


# Load last season stats
df = pd.read_csv("wcc_2425_stats.csv")

# Rename columns
rename_map = {
    "FG": "FGM",
    "FGA": "FGA",
    "3P": "3PM",
    "3PA": "3PA",
    "FT": "FTM",
    "FTA": "FTA",
    "ORB": "OREB",
    "DRB": "DREB",
    "AST": "AST",
    "STL": "STL",
    "BLK": "BLK",
    "TOV": "TO",
    "PTS": "PTS"
}
df = df.rename(columns=rename_map)

# Convert per-game averages → season totals
stats_to_scale = list(rename_map.values())
for stat in stats_to_scale:
    df[stat] = df[stat] * df["G"]

# Calculate fantasy points
df["FantasyPts"] = df.apply(calculate_fantasy_points, axis=1)
df['FP_pg'] = (df['FantasyPts'] / df['G']).round(2)
# Rank leaders
leaders = df[["Player", "Team", "G", "FantasyPts"]].sort_values("FantasyPts", ascending=False)

df.to_csv("lastseason2.csv")
print(leaders.head(10))

