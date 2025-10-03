import pandas as pd

# Load CSV
df = pd.read_csv("rosters/gonzaga_roster_with_images.csv")
df = df.drop(df.columns[0], axis=1)
# Save
df.to_csv("rosters/gonzaga_roster_with_images_cleaned.csv", index=False)
