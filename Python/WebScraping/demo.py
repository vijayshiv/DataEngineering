import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, base_url, num_pages_to_scrape):
        self.base_url = base_url
        self.num_pages_to_scrape = num_pages_to_scrape
        self.data_frames = []

    def scrape_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            name_of_tender = [data.text for data in soup.find_all('h3', class_='Content Type : Reports title')]
            description_of_each_tender = [re.sub(r'\s+', ' ', data.text.replace('\n', '').strip()) for data in soup.find_all('span', class_='nontrimmed')]
            category_of_tender = [data.text.replace('Doc Sub Category :', '') for data in soup.find_all('span', class_='doc-sub-type')]
            country_name_of_tender = [data.text.replace('Country : ', '').strip() if data.text.strip() != '' else None for data in soup.find_all('span', class_='countrylist')]
            content_type = [data.text.replace('Content Type : ', '').strip() for data in soup.find_all('em', class_='post-info')]
            new_content_type = content_type[1::2]
            date_of_tender = [data.text.strip() for data in soup.find_all('em', class_='date')]
            links_of_tender = [a_tag.get('href') for a_tag in soup.find_all('a') if a_tag.get('href') and a_tag.get('href').startswith('http://documents')]

            min_length = min(len(name_of_tender), len(description_of_each_tender), len(category_of_tender), len(country_name_of_tender), len(new_content_type), len(date_of_tender), len(links_of_tender))

            data = {
                'name_of_tender': name_of_tender[:min_length],
                'description': description_of_each_tender[:min_length],
                'category': category_of_tender[:min_length],
                'country': country_name_of_tender[:min_length],
                'content_type': new_content_type[:min_length],
                'date_of_tender': date_of_tender[:min_length],
                'links': links_of_tender[:min_length]
            }

            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            print(f'Error while scraping: {str(e)}')
            return None

    def scrape_pages(self):
        for page_number in range(self.num_pages_to_scrape):
            url = f'{self.base_url}={page_number}'
            print(f'Scraping page {page_number + 1}...')

            # Scrape and process the data for the current page
            page_data = self.scrape_page(url)

            if page_data is not None:
                self.data_frames.append(page_data)

        # Concatenate all DataFrames from different pages into one
        if self.data_frames:
            data_df = pd.concat(self.data_frames, ignore_index=True)
            return data_df
        else:
            print('No data scraped.')
            return None

# Usage example:
base_url = 'https://ieg.worldbankgroup.org/ieg-search?search_api_fulltext=tenders&field_topic=All&field_sub_category=All&content_type_1=&field_organization_tags=All&type_2_op=not&type_2%5B0%5D=homepage_spotlight_feature&sort_by=search_api_relevance&sort_order=DESC&page'
num_pages_to_scrape = 3

scraper = WebScraper(base_url, num_pages_to_scrape)
data_df = scraper.scrape_pages()

if data_df is not None:
    data_df

data_df.to_csv(r'D:\Data Engineering\Python\WebScraping\demo_data.csv', index=False)