
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


# --- SETUP ---
team = 'portland'
driver = webdriver.Chrome()  # or webdriver.Firefox()
driver.get("https://portlandpilots.com/sports/womens-basketball/roster")  # replace with your roster URL
time.sleep(3)


def find_rosterview(driver,visible_text):

    selector = "//select[@id='sidearm-roster-select-template-dropdown']"
    go_button = '//*[@id="sidearm-roster-select-template-button"]'
    # Try each dropdown selector in order until we find one that works

    try:
        # Attempt to locate the dropdown
        dropdown = driver.find_element(By.XPATH, selector)
        select = Select(dropdown)

        # Select the desired option (example: 'Roster View - Grid')
        select.select_by_visible_text(visible_text)
        print(f"Selected {visible_text} using selector: {selector}")
        go_button = driver.find_element(By.XPATH,go_button)
        go_button.click()

        return True  # Success, exit the function

    except NoSuchElementException:
        print(f"Dropdown not found with selector: {selector}\n")

    # If no dropdown was found, raise an error or handle accordingly
    print("No dropdown found on the page.\n")
    return False




def getgridview(driver):
    #need to label the dataframe based on team name and year
    rosterviewgrid = "Roster View - Grid"
    #rosteryear = "2022-23 Women's Basketball Roster"

    try:
        #Get Grid View
        find_rosterview(driver,rosterviewgrid)
    except(ValueError):
        print("<li class> did not work")
        raise Exception 

   
   
    time.sleep(1.1)
    table_data = []
    coaches_list = []
    matches = driver.find_elements(By.TAG_NAME,"tr")

    # Get the first row (headers) to set as column names
    header_row = matches[0].find_elements(By.TAG_NAME, "th")
    headers = [header.text for header in header_row]

    for match in matches:
        cells = match.find_elements(By.TAG_NAME,"td")
        row_data = [cell.text for cell in cells] #extract text from each cell
        if row_data: #append only non-empty rows
            table_data.append(row_data)
    for item in table_data:
        if len(item)<4:
            coaches_list.append(item)
    table_data = [table for table in table_data if len(table)>4]
    time.sleep(.1)
    #driver.quit()
    df = pd.DataFrame(table_data,columns=headers)
    coaches_df = pd.DataFrame(coaches_list)
    coaches_df = coaches_df.dropna()
    try:
        df = df[df['NAME'].str.len()>0]
    except Exception as e:
        print(f"name {e}")
    try:
        df = df[df['FULL NAME'].str.len()>0]
    except Exception as e:
        print(f"Name name : {e}")
    #print(f"Players df : {df}\n")
    #print(f"Coaches_df : {coaches_df} \n")
    df.to_csv(f"rosters/{team}_roster.csv")
    coaches_df.to_csv("coaches/{team}_coaches.csv")
    return df,coaches_df
driver.quit()
getgridview(driver)
