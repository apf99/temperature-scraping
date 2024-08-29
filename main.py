import requests
import selectorlib
from datetime import datetime


URL = 'https://programmer100.pythonanywhere.com/'

def scrape(url):
    # scrape the page
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['home']
    return value


def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')


def get_data():
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        # content = read(extracted)
        # if extracted != 'No upcoming tours':
        #     if not extracted in content:
        #         store(extracted)


if __name__ == '__main__':
    get_data()


