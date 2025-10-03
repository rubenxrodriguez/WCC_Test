# build_all_players.py

import pandas as pd

# --- Load data ---
lastseason = pd.read_csv("test_fantasy_pts/lastseason.csv")
transfers = pd.read_csv("wcc_stats_conf_strength/wcc_transfers.csv")
conf_strength = pd.read_csv("wcc_stats_conf_strength/conf_strength.csv")

# --- Step 1. Add ConfStrength = 0 for all WCC returners ---
lastseason["ConfStrength"] = 0
lastseason["PlayerType"] = "Returner"

# --- Step 2. Clean transfers: remove intra-WCC transfers ---
transfers = transfers[transfers["conferenceShortNameFrom"] != "WCC"].copy()

# --- Step 3. Encode ConfStrength for transfers ---
# Find WCC's rank and stddev
wcc_rank = conf_strength.loc[conf_strength["most_common_conference"] == "WCC", "median_rank"].values[0]
std = conf_strength["median_rank"].std()
print(wcc_rank, std)
def encode_conf_strength(conf_from):
    row = conf_strength.loc[conf_strength["most_common_conference"] == conf_from, "median_rank"]
    if row.empty:
        return 0  # fallback if missing
    rank = row.values[0]
    if rank > wcc_rank + 2*std:
        return -2
    elif rank > wcc_rank + std:
        return -1
    elif rank < wcc_rank:
        return 1
    else:
        return 0

transfers["ConfStrength"] = transfers["conferenceShortNameFrom"].apply(encode_conf_strength)
transfers["PlayerType"] = "Transfer"

# --- Step 3b. Calculate fantasy points for transfers ---
def calc_fantasy(row):
    return (
        1.3 * row["ptsScored"] +
        1.2 * row["reb"] +
        1.5 * row["ast"] +
        3 * row["stl"] +
        3 * row["blk"]
    )

transfers["FantasyPts"] = transfers.apply(calc_fantasy, axis=1)

# --- Step 4. Do name remapping ---
transfers["Player"] = (transfers["firstName"] + " " + transfers["lastName"]).str.strip()

# --- Step 5. Align columns to match lastseason.csv style ---
# We'll keep core columns from transfers; others will be NaN in merged dataset
transfer_rename = {
    "teamMarketFrom": "Team",
    'teamMarketTo': 'NewTeam',
    'conferenceShortNameTo' : 'NewConf',
    "ptsScored": "PTS",
    "reb": "TRB",
    "ast": "AST",
    "stl": "STL",
    "blk": "BLK",
    "mins": "MP"
}
transfers = transfers.rename(columns=transfer_rename)
transfers['conf'] = transfers['conferenceShortNameFrom']
lastseason['conf'] = "WCC"
lastseason['NewTeam'] = pd.NA
lastseason['NewConf'] = pd.NA

# Add missing columns from lastseason so schema matches
for col in lastseason.columns:
    if col not in transfers.columns:
        transfers[col] = pd.NA

# --- Step 6. Union datasets ---
all_players = pd.concat([lastseason, transfers[lastseason.columns]], ignore_index=True)
all_players = all_players[['Player', 'Team','conf', 'Pos', 'NewTeam','NewConf','G', 'GS', 'MP', 'FGM',
       'FGA', 'FG%', '3PM', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FTM',
       'FTA', 'FT%', 'OREB', 'DREB', 'TRB', 'AST', 'STL', 'BLK', 'TO', 'PF',
       'PTS', 'FantasyPts', 'ConfStrength',
       'PlayerType']]
    # Round all numeric columns to 1 decimal
numeric_cols = all_players.select_dtypes(include='number').columns
all_players[numeric_cols] = all_players[numeric_cols].round(1)
# --- Step 7. Save merged file ---
all_players.to_csv("all_players.csv", index=False)

print("✅ all_players.csv created with returners + transfers")
