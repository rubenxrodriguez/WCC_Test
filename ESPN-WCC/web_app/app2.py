
import streamlit as st
import pandas as pd
import glob

st.set_page_config(page_title="WBB Rosters", layout="wide")
st.title("🏀 WCC Women's Basketball Rosters")

# --- Load all roster CSVs ---
files = glob.glob("rosters/*_roster_with_images.csv")
teams = {f.split("/")[-1].replace("_roster_with_images.csv", ""): pd.read_csv(f) for f in files}

# --- Team multiselect ---
team_names = list(teams.keys())
selected_teams = st.multiselect("Select Teams", team_names, default=team_names[:2])

# --- Combine selected teams' data ---
if selected_teams:
    combined_df = pd.concat([teams[t] for t in selected_teams], keys=selected_teams)
    combined_df.reset_index(level=0, inplace=True)
    combined_df.rename(columns={"level_0": "Team"}, inplace=True)

    # --- Player multiselect per team ---
    players_by_team = {}
    for team in selected_teams:
        df_team = combined_df[combined_df["Team"] == team]
        players_by_team[team] = st.multiselect(f"Select players from {team}", df_team["FULL NAME"].tolist())

    # --- Display selected players ---
    max_len = max(len(players) for players in players_by_team.values()) if players_by_team else 0
    for i in range(max_len):
        cols = st.columns([1, 5] * len(selected_teams), gap="small")
        for j, team in enumerate(selected_teams):
            df_team = combined_df[combined_df["Team"] == team]
            players = players_by_team[team]
            if i < len(players):
                player_row = df_team[df_team["FULL NAME"] == players[i]].iloc[0]
                img_col = cols[j*2]
                info_col = cols[j*2 + 1]
                with img_col:
                    if pd.notna(player_row["ImageURL"]):
                        st.image(player_row["ImageURL"], width=120)
                with info_col:
                    st.markdown(
                        f"**{player_row['FULL NAME']}**  \n"
                        f"Pos: {player_row['POS.']} | Ht: {player_row['HT.']} | Year: {player_row['ACADEMIC YEAR']}  \n"
                        f"Hometown: {player_row['HOMETOWN']}  \n"
                        f"Previous School: {player_row.get('PREVIOUS SCHOOL', '—')}"
                    )
