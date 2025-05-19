import requests
from bs4 import BeautifulSoup
import csv


def get_data():
  url = 'https://www.nnvl.noaa.gov/view/globaldata.html'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  data = []
  table = soup.find(id='gtemp_table')
  rows = table.find_all('tr')
  for row in rows:
    data.append([td.text for td in row])

  return data


def main():
  data = get_data()

  with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    # Write the header
    writer.writerows(data)


if __name__ == '__main__':
  main()
