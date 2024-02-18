from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Set up the Selenium webdriver
chromedriver_path = r'C:\Users\ACER\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

service = ChromeService(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL of the webpage with JavaScript-rendered content
url = "http://en.chinabidding.mofcom.gov.cn/channel/EnSearchList.shtml?keyword=tenders"  

# Open the webpage using Selenium
driver.get(url)

# Wait for the page to fully load (you can adjust the wait time as needed)
driver.implicitly_wait(10)  # Wait for up to 10 seconds for the page to load

# Execute JavaScript if needed
# For example, you can scroll to load more content:
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Extract the HTML content after the page is fully loaded
page_source = driver.page_source

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(page_source, 'html.parser')

# Locate and extract the data using BeautifulSoup
# For example, find elements by their CSS selector
elements = soup.find_all('div')
print(elements)
# Process and print or store the extracted data
# for element in elements:
#     data = element.text.strip()
#     print(data)

# Close the Selenium webdriver
driver.quit()
