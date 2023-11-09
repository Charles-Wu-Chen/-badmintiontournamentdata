import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# import pkg_resources
import csv

datestring = "20230819"

# URL of the tournament players page
url = "https://www.tournamentsoftware.com/tournament/cfbb2654-8db8-4b4d-988b-e19225bc12f7/matches/"+datestring


# Initialize a headless browser using Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in the background
# driver_path = pkg_resources.resource_filename(__name__, "chromedriver.exe")
# print(driver_path)
# browser = webdriver.Chrome(executable_path=driver_path, options=options)
# browser = webdriver.Chrome(executable_path="c:\\Users\\wuche\\OneDrive\\Documents\\selenium\\chromedriver.exe", options=options)
browser = webdriver.Chrome(ChromeDriverManager().install())
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
with open(datestring+'output.html', 'w', encoding='utf-8') as file:
    file.write(str(html_content))
