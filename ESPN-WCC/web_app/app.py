import streamlit as st
import pandas as pd

# Load the roster CSV
df = pd.read_csv("rosters/gonzaga_roster_with_images.csv")

st.set_page_config(page_title="Gonzaga Roster", layout="wide")

st.title("🏀 Gonzaga Women's Basketball Roster")

# Display roster in a grid with images
for _, row in df.iterrows():
    cols = st.columns([1, 5], gap = 'small')  # two-column layout (image | info)
    with cols[0]:
        if pd.notna(row["ImageURL"]):
            st.image(row["ImageURL"], width=150)
    with cols[1]:
        st.markdown(f"**{row['FULL NAME']}**  \n"
                    f"Pos: {row['POS.']} | Ht: {row['HT.']} | Year: {row['ACADEMIC YEAR']}  \n"
                    f"Hometown: {row['HOMETOWN']}  \n"
                    f"Previous School: {row.get('PREVIOUS SCHOOL', '—')}")

