import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# import pkg_resources
import csv


class Match:
    def __init__(self, match_type, match_round, team1_player1_name, team1_player1_link, team1_player2_name, team1_player2_link, team2_player1_name, team2_player1_link, team2_player2_name, team2_player2_link, team1_result, team1_score,  team2_result, team2_score, link):
        self.match_type = match_type
        self.match_round = match_round
        self.team1_player1_name = team1_player1_name
        self.team1_player1_link = team1_player1_link 
        self.team1_player2_name = team1_player2_name
        self.team1_player2_link  = team1_player2_link 
        self.team1_result = team1_result
        self.team1_score = team1_score
        self.team2_player1_name = team2_player1_name
        self.team2_player1_link  = team2_player1_link 
        self.team2_player2_name = team2_player2_name
        self.team2_player2_link = team2_player2_link 
        self.team2_result = team2_result
        self.team2_score = team2_score
        self.link = link

datestring = "20230819"
# Read HTML content from the file
with open(datestring+'output.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Send an HTTP GET request to the URL
# response = requests.get(url)

# Parse the content of the response using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
# print(soup)
# Find the table that contains player information

match_list = []

matches = soup.find_all("li", class_="match-group__item")
for match in matches:
    print("``````````````````match``````````````````")
    # print(match)
    # match_type = match.find('span', class_='nav-link__value').text
    # print(match_type)
    match_type = match.select_one('span.nav-link__value').text
    print(f'match type: {match_type}')

    # Extract match round
    match_round = match.select_one('span.nav-link[title]').text
    print(f'match round: {match_round}')



    team1_result = ''
    team2_result = ''
    match_rows = match.select('div.match__row')
    if 'has-won' in match_rows[0].get('class'):
        team1_result = 'W'
        print(f'team1 result: {team1_result}')
    if 'has-won' in match_rows[1].get('class'):
        team2_result = 'W'
        
        print(f'team2 result: {team2_result}')
    
    #matches > div.module__content > div > ol > li > div > ol > li:nth-child(286) > div > div.match__body > div.match__row-wrapper > div.match__row.has-won
    #matches > div.module__content > div > ol > li > div > ol > li:nth-child(27) > div > div.match__body > div.match__row-wrapper
    arr_player = match.select('span.match__row-title-value-content')
    # print(arr_player)
    # print(len(arr_player))
# todo chatgpt to refactor code ?

    team1_player2_name = ''
    team1_player2_link = ''
    team2_player2_name = ''
    team2_player2_link = ''
    team1_player1_name = ''
    team1_player1_link = ''
    team2_player1_name = ''
    team2_player1_link = ''

    if len(arr_player) == 2:
        
        team1_player1_name = arr_player[0].select_one('span.nav-link__value').text
        team1_player1_link = arr_player[0].select_one('a.nav-link')['href']
        team2_player1_name = arr_player[1].select_one('span.nav-link__value').text
        team2_player1_link = arr_player[1].select_one('a.nav-link')['href']

        
    elif len(arr_player) == 4:
        team1_player1_name = arr_player[0].select_one('span.nav-link__value').text
        team1_player1_link = arr_player[0].select_one('a.nav-link')['href']
        
        team1_player2_name = arr_player[1].select_one('span.nav-link__value').text
        team1_player2_link = arr_player[1].select_one('a.nav-link')['href']

        team2_player1_name = arr_player[2].select_one('span.nav-link__value').text
        team2_player1_link = arr_player[2].select_one('a.nav-link')['href']
        
        team2_player2_name = arr_player[3].select_one('span.nav-link__value').text
        team2_player2_link = arr_player[3].select_one('a.nav-link')['href']
    
    else :
        continue

    #matches > div.module__content > div > ol > li > div > ol > li:nth-child(1) > div > div.match__body > div.match__result
    # match_result = match.select('div.match__result')
    # print(match_result)
    points = match.select('li.points__cell')
    # print(points)
    team1_score=''
    team2_score=''

    if points:
        # team1_score = points[0]
        team1_score = int(points[0].text.strip())
        team2_score = int(points[1].text.strip())
    print(f'team1_score: {team1_score}; team2_score: {team2_score}')

    match_list.append(Match(match_type, match_round, team1_player1_name, team1_player1_link, team1_player2_name, team1_player2_link, 
                             team2_player1_name, team2_player1_link, team2_player2_name, team2_player2_link, team1_result, team1_score,  team2_result, team2_score, len(arr_player)))



for idx, match in enumerate(match_list):
    print(f"{idx} : {match.__dict__}")

csv_file_name = datestring+'match.csv'
# Extract field names from the Player class attributes
fieldnames = ['match_type', 'match_round', 'team1_player1_name', 'team1_player1_link', 'team1_player2_name', 'team1_player2_link', 
              'team2_player1_name', 'team2_player1_link', 'team2_player2_name', 'team2_player2_link', 'team1_result', 'team1_score', 'team2_result', 'team2_score', 'link']

with open(csv_file_name, 'w', newline='') as csvfile:
    # Create a DictWriter object and specify the fieldnames
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    csvwriter.writeheader()

    # Write the data rows
    for match in match_list:
        csvwriter.writerow(match.__dict__)
