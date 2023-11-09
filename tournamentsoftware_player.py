import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# import pkg_resources
import csv


class Player:
    def __init__(self, name, link, club, memberId):
        self.name = name
        self.club = club
        self.link = link
        self.memberId = memberId


# URL of the tournament players page
url = "https://www.tournamentsoftware.com/tournament/CFBB2654-8DB8-4B4D-988B-E19225BC12F7/players"


# Initialize a headless browser using Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in the background
# driver_path = pkg_resources.resource_filename(__name__, "chromedriver.exe")
# print(driver_path)
# browser = webdriver.Chrome(executable_path=driver_path, options=options)
browser = webdriver.Chrome(executable_path="c:\\Users\\wuche\\OneDrive\\Documents\\selenium\\chromedriver.exe", options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(options=options)
browser.get(url)

# Check if the page has a cookie acceptance popup
button_element = browser.find_element_by_css_selector("button.btn.btn--success.js-accept-basic")

if button_element:
    # Handle the cookie acceptance (click the "Accept" button, for example)
    # accept_button = driver.find_element_by_id('accept-button')  # Example accept button ID
    button_element.click()

# Get the HTML content of the page using the driver
html_content = browser.page_source

# Print the HTML content
# print(html_content)


# Send an HTTP GET request to the URL
# response = requests.get(url)

# Parse the content of the response using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
# print(soup)
# Find the table that contains player information

players_list = []

players = soup.find_all("li", class_="list__item js-alphabet-list-item")
for player in players:
    name = player.find("span", class_="nav-link__value").text
    link = player.find("a", class_="nav-link media__link")["href"]
    club_info = player.find("div", class_="media__subheading-wrapper")
    club = club_info.find("span", class_="nav-link__value").text
    players_list.append(Player(name, link, club, ""))

for idx, player in enumerate(players_list):
    print(f"{idx} : {player.__dict__}")

csv_file_name = 'player_CFBB2654.csv'
# Extract field names from the Player class attributes
fieldnames = ['name', 'link', 'club', 'memberId']

with open(csv_file_name, 'w', newline='') as csvfile:
    # Create a DictWriter object and specify the fieldnames
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    csvwriter.writeheader()

    # Write the data rows
    for player in players_list:
        csvwriter.writerow(player.__dict__)
