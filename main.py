import requests
import selectorlib
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

URL = 'https://programmer100.pythonanywhere.com/'

# Establish a connection
connection = sqlite3.connect('temperatures.db')

def scrape(url):
    # scrape the page
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['home']
    return value


def store(date, temperature):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO readings VALUES(?,?)', (date, temperature))
    connection.commit()


def get_data():
    scraped = scrape(URL)
    temperature = extract(scraped)
    date = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    store(date, temperature)


st.title('Temperature Data')
button = st.button('Get Data')
if button:
    get_data()

cursor = connection.cursor()
cursor.execute('SELECT * FROM readings')
results = cursor.fetchall()
dates = [item[0] for item in results]
temperatures = [item[1] for item in results]

labels = {'x': 'Dates', 'y':'Temperature (C)'}
figure = px.line(x=dates, y=temperatures, labels=labels)
st.plotly_chart(figure)

