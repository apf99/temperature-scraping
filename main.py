import requests
import selectorlib
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px

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
    with open('data.csv', 'a') as file:
        file.write(extracted + '\n')


def get_data():
        scraped = scrape(URL)
        extracted = extract(scraped)
        now = datetime.now()
        result = f'{now.strftime('%y-%m-%d-%H-%M-%S')},{extracted}'
        print(result)
        store(result)


st.title('Temperature Data')
#get the data
button = st.button('Get Data')
if button:
    get_data()

df = pd.read_csv('data.csv')
temperatures = df.temperatures
dates = df.dates
labels = {'x': 'Dates', 'y': 'Temperature (C)'}
figure = px.line(x=dates, y=temperatures, labels=labels)
st.plotly_chart(figure)

