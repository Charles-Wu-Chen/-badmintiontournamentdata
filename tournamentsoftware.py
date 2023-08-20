import requests
from bs4 import BeautifulSoup

# URL of the tournament players page
url = "https://www.tournamentsoftware.com/tournament/CFBB2654-8DB8-4B4D-988B-E19225BC12F7/players"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    # Find the table that contains player information
    player_table = soup.find("table", class_="table-main")

    # Iterate through each row in the table
    for row in player_table.find_all("tr")[1:]:  # Skip the header row
        columns = row.find_all("td")
        
        # Extract the desired information from the columns
        player_name = columns[0].text.strip()
        player_country = columns[1].text.strip()
        player_seed = columns[2].text.strip()
        
        print("Player Name:", player_name)
        print("Country:", player_country)
        print("Seed:", player_seed)
        print("-" * 30)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
