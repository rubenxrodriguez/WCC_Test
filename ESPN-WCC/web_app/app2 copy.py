import streamlit as st
import pandas as pd
import glob

st.set_page_config(page_title="WBB Rosters", layout="wide")

st.title("🏀 WCC Women's Basketball Rosters")

# --- Load all roster CSVs ---
files = glob.glob("rosters/*_roster_with_images.csv")
teams = {f.split("/")[-1].replace("_roster_with_images.csv", ""): pd.read_csv(f) for f in files}

# Pick 3 teams to show side by side
team_names = list(teams.keys())
selected_teams = team_names[:2]  # first 3, or you can make this a st.multiselect

dfs = [teams[name] for name in selected_teams]

# Find the max roster length among the teams so we can iterate cleanly
max_len = max(len(df) for df in dfs)

for i in range(max_len):
    cols = st.columns([1, 5, 1, 5, 1, 5], gap="small")
    
    for j, df in enumerate(dfs):
        if i < len(df):  # only render if that team has a player at this index
            row = df.iloc[i]
            img_col = cols[j*2]
            info_col = cols[j*2 + 1]

            with img_col:
                if pd.notna(row["ImageURL"]):
                    st.image(row["ImageURL"], width=120)
            with info_col:
                st.markdown(
                    f"**{row['FULL NAME']}**  \n"
                    f"Pos: {row['POS.']} | Ht: {row['HT.']} | Year: {row['ACADEMIC YEAR']}  \n"
                    f"Hometown: {row['HOMETOWN']}  \n"
                    f"Previous School: {row.get('PREVIOUS SCHOOL', '—')}"
                )
