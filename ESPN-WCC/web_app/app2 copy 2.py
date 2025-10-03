import streamlit as st
import pandas as pd
import glob

st.set_page_config(page_title="WBB Rosters", layout="wide")

st.title("🏀 WCC Women's Basketball Rosters")

# --- Load all roster CSVs ---
files = glob.glob("rosters/*_roster_with_images.csv")
teams = {f.split("/")[-1].replace("_roster_with_images.csv", ""): pd.read_csv(f) for f in files}

# --- Multiselect for teams ---
team_names = list(teams.keys())
selected_teams = st.multiselect(
    "Select up to 3 teams to display",
    options=team_names,
    default=team_names[:3],  # default selection
    help="You can select 1, 2, or 3 teams"
)

# Limit to 3 teams max
selected_teams = selected_teams[:3]

dfs = [teams[name] for name in selected_teams]

# --- Find the max roster length among the selected teams ---
if dfs:
    max_len = max(len(df) for df in dfs)

    for i in range(max_len):
        # 2 columns per team: image + info
        cols = st.columns([1, 5]*len(dfs), gap="small")
        
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
else:
    st.info("Select at least one team to display.")
