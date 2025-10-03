from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime



def get_indices(rows_text):
    starters_counter = 0
    team_counter = 0
    firstplayerindex1=firstplayerindex2=lastplayerindex1=lastplayerindex2 = 0
    while(True):
        if starters_counter<1 and team_counter<1 :
            #then the next row and up to "TEAM" will be Team1 Names
            firstplayerindex1 = rows_text.index("STARTERS")+1
            lastplayerindex1 = rows_text.index("TEAM")-1
            starters_counter+=1
            team_counter+=1
        else:
            look = rows_text[lastplayerindex1+2:]
            firstplayerindex2 = look.index("STARTERS")+1+lastplayerindex1+2
            #print(look.index("TEAM"))
            lastplayerindex2 = look.index('TEAM')-1+lastplayerindex1+2
            break
    firststatsindex1 = lastplayerindex1 + 3
    laststatsindex1 = firststatsindex1 + (lastplayerindex1-firstplayerindex1+1)

    firststatsindex2 = lastplayerindex2 + 3
    laststatsindex2 = firststatsindex2 + (lastplayerindex2-firstplayerindex2+1) #these are the indices but if we want to graph the rows we use range(firststatsindex2,laststatsindex2+1)
    return firstplayerindex1,lastplayerindex1,firststatsindex1,laststatsindex1,firstplayerindex2,lastplayerindex2,firststatsindex2,laststatsindex2
def process_team_data(player_rows, name_start, name_end, stats_start, stats_end):
    # Process player names
    #Grabs the whole line for player name
    names = [player.text.replace("\n", " ") for player in player_rows[name_start:name_end]]
    names.pop(5)  # Remove element at index 5
    positions = [name[-1:] for name in names]
    names = [name[:-2] for name in names]
    # Process player stats
    stats = [player.text.replace("\n", " ") for player in player_rows[stats_start:stats_end]]
    stats.pop(6)
    
    # Extract column names
    colnames = stats[0].split(' ')
    colnames.insert(0, "Name")
    colnames.insert(1,"Position")
    stats.pop(0)

    # Create a list of player stats
    player_stats = []
    for i in range(len(stats)):
        temp_stats = stats[i].split(" ")
        temp_stats.insert(0, names[i])
        temp_stats.insert(1,positions[i])
        player_stats.append(temp_stats)

    # Create a DataFrame
    df = pd.DataFrame(player_stats, columns=colnames)


    
    return df

def calculate_fantasy_points(row):
    #print(row["Name"])
    # Define rules for calculating fantasy points for each stat
    points_dict = {
        'FGM' : 2,
        'FGA' :-1,
        'FTM' : 1,
        'FTA' : -1,
        '3PM': 1,  
        'REB':1,
        'AST': 2,
        'STL': 4,
        'BLK': 4,
        'TO':-2,
        'PTS': 1,
        'Result':1
        
    }

    fantasy_points = 0
    for stat, value in row.items():
        if stat in points_dict:
           
            fantasy_points += points_dict[stat] * int(value)

    return fantasy_points


def row_of_player(player_name, team_df):
    # Assuming 'Name' is the column containing player names
    for index, row in team_df.iterrows():
        if row['Name'] == player_name:
            return row

    return None  # Return None if player not found
#print(team2_df)


from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


def scrape_dailyboxscores(websites,csv_file_name,folder_path,playername_mapping,userteam_mapping):
    """
    Scrape daily box scores from a list of websites and save the data to CSV files.

    Parameters:
    - websites (list): List of URLs for daily box score pages.
    - csv_file_name (str): The name to use when saving the CSV file.
    - folder_path (str): The folder path where the CSV file will be saved.
    - playername_mapping (dict): A dictionary mapping player names.
    - userteam_mapping (dict): A dictionary mapping user teams.

    Returns:
    - pd.DataFrame: A DataFrame containing the scraped data.
    """
    formatted_date = 'N/A'
    dataframes = []
    for website in websites:
        i = 1
        while(True):

            driver = webdriver.Chrome()
            driver.get(website)
          
            xpatha = f'/html/body/div[1]/div/div/div/div/main/div[3]/div/div/div[1]/div/div/section/div/section[{i}]/div[2]/a[2]'
                      
            xpathb = '/html/body/div[1]/div/div/div/div/main/div[3]/div/div/div[1]/div/div/section/header/div[1]'
            
            try:
                #Find the box score button

                try:
                    #finds the box score button
                    xpatha_ = driver.find_element(By.XPATH, xpatha)
                   # xpatha_.click()
                        

                except (NoSuchElementException, ValueError):
                    print("Button cannot be found.\n")
                    break

                #Get the Date from the scoreboard page
                try:
                    xpathb_ = driver.find_element(By.XPATH, xpathb).text
                    
                    # Try to convert the string to a datetime object
                    date_object = datetime.strptime(xpathb_, '%A, %B %d, %Y')
                    # Format the datetime object as 'MM/DD/YY'
                    formatted_date = date_object.strftime('%m/%d/%y')
                    

                except (NoSuchElementException, ValueError):
                    print("Date not found with outer div class.\n")
                #Now we should have the date, so we click on box score.
                xpatha_.click()
                # ----------------------------Extract the box score from the Box Score Page----------------------
                time.sleep(1.5)
                player_rows = driver.find_elements(By.CLASS_NAME, "Table__TR.Table__TR--sm.Table__even")
                time.sleep(0.9)
                rows_text = [player.text for player in player_rows]

                namestart1, nameend1, statstart1, statend1, namestart2, nameend2, statstart2, statend2 = get_indices(rows_text)

                team1_df = process_team_data(player_rows, namestart1, nameend1 + 1, statstart1, statend1 + 1)
                                                                
                fullteamname1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div/div[5]/div/div[1]/section/div/div/div/div[1]/div/div[1]/div').text
                fullteamname2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div/div[5]/div/div[1]/section/div/div/div/div[2]/div/div[1]/div').text
                                                                
                team1_df.insert(2, "Team", fullteamname1)
                team1_df.insert(3, "Date", formatted_date)
                team1_df.insert(len(team1_df.columns) - 1, "Opponent", fullteamname2)
                team1_df['Name'] = team1_df.apply(lambda row: playername_mapping.get((row['Name'], row['Team']), row['Name']), axis=1)
                 # Split 'FG' into 'FGM' and 'FGA'
                team1_df[['FGM', 'FGA']] = team1_df['FG'].str.split('-', expand=True)
                  # Split 'FT' into 'FTM' and 'FTA'
                team1_df[['FTM', 'FTA']] = team1_df['FT'].str.split('-', expand=True)

                 # Split '3PT' into '3PM' and '3PA'
                team1_df[['3PM', '3PA']] = team1_df['3PT'].str.split('-', expand=True)

                #check if team1 won add a new column of len(team1_df.rows) of 1

                # Add a new column 'FantasyPts' and calculate fantasy points for each player
                team1_df['FantasyPts'] = team1_df.apply(calculate_fantasy_points, axis=1)

                 # Reorder columns
                col_order = ['Name','Team','User Team','FantasyPts','Date','Opponent','MIN', 'FGM', 'FGA', '3PM', '3PA', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
                team1_df = team1_df[col_order]
                
                print(team1_df.head())
                team2_df = process_team_data(player_rows, namestart2, nameend2 + 1, statstart2, statend2 + 1)
                team2_df.insert(2, "Team", fullteamname2)
                team2_df.insert(3, "Date", formatted_date)
                team2_df.insert(len(team2_df.columns) - 1, "Opponent", fullteamname1)
                team2_df['Name'] = team2_df.apply(lambda row: playername_mapping.get((row['Name'], row['Team']), row['Name']), axis=1)

                # Append the dataframes to the concatenated_df
                dataframes.append(team1_df)
                dataframes.append(team2_df)
            except Exception as e:
                    print(f"An error occurred: {str(e)}")

            driver.quit()
            i+=1  
        print(f"-----\nEnd of Day {formatted_date}\n-----")  
    # Write the concatenated data to a CSV file
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    concatenated_df['User Team'] = concatenated_df.apply(lambda row: userteam_mapping.get((row['Name'], row['Team']), 'FA'), axis=1) #uses userteam_mapping to map the players to the appropriate team
                                                                                    #default value for Team is FA
    os.makedirs(folder_path,exist_ok = True)
    csv_file_path = os.path.join(folder_path,csv_file_name)
    concatenated_df.to_csv(csv_file_path, index=False, mode='w', header=True)
    

    return concatenated_df

dates_list_wk1 = ['1106', '1107', '1108', '1109', '1110', '1111', '1112']
dates_list_wk2 = ['1113', '1114', '1115', '1116', '1117', '1118', '1119']
'''
for i in range(3,8):
    dates_list = locals()[f'dates_list_wk{i}']
    websites = [f'https://www.espn.com/womens-college-basketball/scoreboard/_/date/2023{date}' for date in dates_list]
    csv_file_name = f'Boxscores_week{i}.csv'
    folder_path = f'Boxscores_week{i}'
    df_result = scrape_dailyboxscores(websites=websites,csv_file_name=csv_file_name,folder_path=folder_path,playername_mapping=playername_mapping,userteam_mapping=userteam_mapping)
'''

import os


def remove_numbers(input_string):
    return ''.join(char for char in input_string if not char.isdigit())


def scrape_dailyboxscores(websites,csv_file_name,folder_path,playername_mapping,userteam_mapping):
    """
    Scrape daily box scores from a list of websites and save the data to CSV files.

    Parameters:
    - websites (list): List of URLs for daily box score pages.
    - csv_file_name (str): The name to use when saving the CSV file.
    - folder_path (str): The folder path where the CSV file will be saved.
    - playername_mapping (dict): A dictionary mapping player names.
    - userteam_mapping (dict): A dictionary mapping user teams.

    Returns:
    - pd.DataFrame: A DataFrame containing the scraped data.
    """
    formatted_date = 'N/A'
    dataframes = []
    for website in websites:
        i = 1
        while(True):

            driver = webdriver.Chrome()
            driver.get(website)
            xpatha = f'/html/body/div[1]/div/div/div/main/div[3]/div/div/div/div/section/div/section[{i}]/div[2]/a[2]'
                    
            xpathb = '/html/body/div[1]/div/div/div/main/div[3]/div/div/div/div/section/header/div[1]'
            
            try:
                #Find the box score button

                try:
                    #finds the box score button
                    xpatha_ = driver.find_element(By.XPATH, xpatha)
                        

                except (NoSuchElementException, ValueError):
                    print("Button cannot be found.\n")
                    break

                #Get the Date from the scoreboard page
                try:
                    xpathb_ = driver.find_element(By.XPATH, xpathb).text
                    
                    # Try to convert the string to a datetime object
                    date_object = datetime.strptime(xpathb_, '%A, %B %d, %Y')
                    # Format the datetime object as 'MM/DD/YY'
                    formatted_date = date_object.strftime('%m/%d/%y')
                    

                except (NoSuchElementException, ValueError):
                    print("Date not found with outer div class.\n")
                #Now we should have the date, so we click on box score.
                xpatha_.click()
                # ----------------------------Extract the box score from the Box Score Page----------------------
                player_rows = driver.find_elements(By.CLASS_NAME, "Table__TR.Table__TR--sm.Table__even")
                time.sleep(0.9)
                rows_text = [player.text for player in player_rows]

                namestart1, nameend1, statstart1, statend1, namestart2, nameend2, statstart2, statend2 = get_indices(rows_text)

                team1_df = process_team_data(player_rows, namestart1, nameend1 + 1, statstart1, statend1 + 1)

                fullteamname1 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[2]/div/div/div[5]/div/div/section[1]/div/div/div/div[1]/div/div[1]/div[1]').text
                fullteamname2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div/div/div[5]/div/div/section[1]/div/div/div/div[2]/div/div[1]/div[1]').text

                team1_df.insert(2, "Team", fullteamname1)
                team1_df.insert(3, "Date", formatted_date)
                team1_df.insert(len(team1_df.columns) - 1, "Opponent", fullteamname2)
                team1_df['Name'] = team1_df.apply(lambda row: playername_mapping.get((row['Name'], row['Team']),row['Name']), axis=1)
                print(team1_df.head())
                team2_df = process_team_data(player_rows, namestart2, nameend2 + 1, statstart2, statend2 + 1)
                team2_df.insert(2, "Team", fullteamname2)
                team2_df.insert(3, "Date", formatted_date)
                team2_df.insert(len(team2_df.columns) - 1, "Opponent", fullteamname1)
                team2_df['Name'] = team2_df.apply(lambda row: playername_mapping.get((row['Name'], row['Team']), row['Name']), axis=1)

                # Append the dataframes to the concatenated_df
                dataframes.append(team1_df)
                dataframes.append(team2_df)
            except Exception as e:
                    print(f"An error occurred: {str(e)}")

            driver.quit()
            i+=1  
        print(f"-----\nEnd of Day {formatted_date}\n-----")  
    # Write the concatenated data to a CSV file
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    concatenated_df['User Team'] = concatenated_df.apply(lambda row: userteam_mapping.get((row['Name'], row['Team']), 'FA'), axis=1) #uses userteam_mapping to map the players to the appropriate team
                                                                                    #default value for Team is FA
    os.makedirs(folder_path,exist_ok = True)
    csv_file_path = os.path.join(folder_path,csv_file_name)
    concatenated_df.to_csv(csv_file_path, index=False, mode='w', header=True)
    

    return concatenated_df


def scrape_and_save2(player_name, team, concatbox_df, folder_path, userteam_mapping):
    
    # Check if the player is in the list and map to userteam
    key = (player_name, team)
    if key in userteam_mapping:
        userteam = userteam_mapping[key]
        # Create a folder for the userteam if it doesn't exist
        userteam_folder = os.path.join(folder_path, userteam)
        os.makedirs(userteam_folder, exist_ok=True)

        # Append the game performance to the existing Excel sheet
        excel_file = os.path.join(userteam_folder, f"{player_name}.xlsx")

        # Read existing data from the Excel file (if it exists)
        existing_df = pd.DataFrame()
        if os.path.exists(excel_file):
            existing_df = pd.read_excel(excel_file, sheet_name="Game", engine='openpyxl')

            # Concatenate the existing data with the new performance data
            combined_df = pd.concat([existing_df, concatbox_df], ignore_index=True, sort=False)

            # Sort the combined DataFrame by the "Date" column
            combined_df.sort_values(by="Date", inplace=True)

            # Add a new column 'FantasyPts' and calculate fantasy points for each player
            combined_df['FantasyPts'] = combined_df.apply(calculate_fantasy_points, axis=1)

            # Write the combined DataFrame to the Excel file
            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                combined_df.to_excel(writer, sheet_name="Game", index=False)
        else:
            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
                concatbox_df.to_excel(writer, sheet_name="Game", index=False)
                # Add a new column 'FantasyPts' and calculate fantasy points for each player
                concatbox_df['FantasyPts'] = concatbox_df.apply(calculate_fantasy_points, axis=1)
                concatbox_df.to_excel(writer, sheet_name="Game", index=False)
    else:
        # Player is not mapped to a user team (Free Agent)
        free_agents_folder = os.path.join(folder_path, "FreeAgents")
        os.makedirs(free_agents_folder, exist_ok=True)

        # Append the player's performance data to the Free Agents Excel file
        free_agents_file = os.path.join(free_agents_folder, f"{player_name}.xlsx")

        # Read existing data from the Free Agents Excel file (if it exists)
        free_agents_df = pd.DataFrame()
        if os.path.exists(free_agents_file):
            free_agents_df = pd.read_excel(free_agents_file, engine='openpyxl')

        # Concatenate the existing data with the new performance data
        combined_df = pd.concat([free_agents_df, concatbox_df], ignore_index=True, sort=False)

        # Sort the combined DataFrame by the "Date" column
        combined_df.sort_values(by="Date", inplace=True)

        # Add a new column 'FantasyPts' and calculate fantasy points for each player
        combined_df['FantasyPts'] = combined_df.apply(calculate_fantasy_points, axis=1)

        # Write the combined DataFrame to the Free Agents Excel file
        with pd.ExcelWriter(free_agents_file, engine='openpyxl', mode='w') as writer:
            combined_df.to_excel(writer, sheet_name="Game", index=False)



def readandconcat_teams(folder_path):
    """
    Read and concatenate data from Excel files within user team folders.

    Parameters:
    - folder_path (str): The path to the main folder containing user team subfolders.

    Returns:
    pd.DataFrame: A DataFrame containing concatenated data from all user teams.
    
    The function iterates through each user team folder, reads all Excel files within each
    folder, concatenates the data, and returns a DataFrame. The resulting DataFrame includes
    data from all user teams, and each row represents a player. The columns include 'Name',
    'Team', 'UserTeam', and 'FantasyPts'.
    """
    all_team_dfs = []
    counter = 0
    # Iterate through each user team folder
    for user_team in os.listdir(folder_path):
        user_team_folder = os.path.join(folder_path, user_team)

        # Skip non-directory items in the folder
        if not os.path.isdir(user_team_folder):
            continue

        team_dfs = []

        # Iterate through each Excel file in the user team folder
        for file_name in os.listdir(user_team_folder):
            if file_name.endswith('.xlsx'):
                file_path = os.path.join(user_team_folder, file_name)

                # Read the Excel file into a DataFrame
                df = pd.read_excel(file_path)

                # Add the DataFrame to the list for the current team
                team_dfs.append(df)
            counter +=1
            if counter%137==0:
                print(f'counter is at {counter}')   

        # Concatenate all DataFrames for the current team
        concat_team_df = pd.concat(team_dfs, ignore_index=True)

        # Append the concatenated DataFrame to the list for all teams
        all_team_dfs.append(concat_team_df)
        counter +=1
        if counter%137==0:
            print(f'counter is at {counter}')

    # Concatenate all DataFrames for all teams
    all_teams_df = pd.concat(all_team_dfs, ignore_index=True)

    # Select desired columns
    # Split 'FG' into 'FGM' and 'FGA'
    all_teams_df[['FGM', 'FGA']] = all_teams_df['FG'].str.split('-', expand=True)

    # Split '3PT' into '3PM' and '3PA'
    all_teams_df[['3PM', '3PA']] = all_teams_df['3PT'].str.split('-', expand=True)

    # Reorder columns
    selected_columns = ['Name','Team','User Team','FantasyPts','Date','Opponent','MIN', 'FGM', 'FGA', '3PM', '3PA', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']

    # Ensure the columns are in the desired order
    result_df = all_teams_df[selected_columns]

    return result_df

