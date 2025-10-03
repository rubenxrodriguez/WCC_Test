import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re
import pandas as pd


driver= webdriver.Chrome()
driver.get("https://gozags.com/sports/womens-basketball/roster")
# //*[@id="main-content"]/article/div[4]/div/div[2]/div/div[1]/section/ul/li[1]/div/div[1]/div[1]/a/img
els =  driver.find_elements(By.TAG_NAME, 'img')
for el in els:
    print("Classes:", el.get_attribute("class"))
    print("Source:", el.get_attribute("src"))
time.sleep(.5)



# - -------------------------------------------------
import requests
from PIL import Image
from io import BytesIO

url = "https://images.sidearmdev.com/resize?url=https%3a%2f%2fdxbhsrqyrr690.cloudfront.net%2fsidearm.nextgen.sites%2fgozags.com%2fimages%2f2025%2f9%2f10%2fpaige_lofing-2059.JPG&width=80&type=webp&quality=90"

response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()

# - -------------------------------------------------
import streamlit as st

url = "https://images.sidearmdev.com/resize?url=https%3a%2f%2fdxbhsrqyrr690.cloudfront.net%2fsidearm.nextgen.sites%2fgozags.com%2fimages%2f2025%2f9%2f10%2fpaige_lofing-2059.JPG&width=80&type=webp&quality=90"

st.image(url, caption="Paige Lofing", width=150)

# - -------------------------------------------------
from IPython.display import Image, display

url = "https://images.sidearmdev.com/resize?url=https%3a%2f%2fdxbhsrqyrr690.cloudfront.net%2fsidearm.nextgen.sites%2fgozags.com%2fimages%2f2025%2f9%2f10%2fpaige_lofing-2059.JPG&width=80&type=webp&quality=90"

display(Image(url=url))


time.sleep(.5)