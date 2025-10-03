import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
import os 

team = 'santa clara'

df = pd.read_csv(f'rosters/{team}_roster.csv')
# Normalize roster names for matching
df["name_key"] = df["FULL NAME"].str.lower().str.replace(r"[^a-z\s]", "", regex=True)

# --- SETUP ---
driver = webdriver.Chrome()  # or webdriver.Firefox()
driver.get("https://santaclarabroncos.com/sports/womens-basketball/roster")  # replace with your roster URL

# --- SCROLL TO LOAD LAZY IMAGES ---
SCROLL_PAUSE = 1.0  # seconds
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# --- COLLECT IMAGES ---
images = driver.find_elements(By.TAG_NAME, "img")

#portland 35:55
i = 0 

for img in images[42:68]:
    i+=1
    src = img.get_attribute("src")
    if not src:
        src = img.get_attribute("data-src")
    if not src:
        continue  # skip if still None

    if "cloudfront.net" not in src:
        continue  # skip non-cloudfront images

    # Clean up filename to compare with roster
    match = re.search(r"/([^/]+?)(?:[-_]\d+)?\.(?:jpg|jpeg|png)", src, re.IGNORECASE)
    if not match:
        continue

    filename_key = match.group(1).replace("_", " ").lower()

    # Try to match against roster names
    for i, row in df.iterrows():
        name_key = row["name_key"]
        if all(part in filename_key for part in name_key.split()):
            df.loc[i, "ImageURL"] = src
            break


''' # How to fix portland's base url problem
# Define the base domain for this team/site
base_url = "https://portlandpilots.com"

# Fix relative URLs
def fix_url(src):
    if pd.isna(src):
        return src
    if src.startswith("http"):
        return src
    return base_url + src  # prepend base if it's relative

df["ImageURL"] = df["ImageURL"].apply(fix_url)

# Save updated CSV
df.to_csv("portland_roster_fixed.csv", index=False)
'''
# Save updated roster with images
df.drop(columns=["name_key"], inplace=True)
df.to_csv(f"rosters/{team}_roster_with_images.csv", index=False)

print(df[["FULL NAME", "ImageURL"]])


driver.quit()
