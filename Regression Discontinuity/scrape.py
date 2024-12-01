from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup, Comment
# import sqlalchemy
import requests
# from dag import Node, Edge, PageContent
# from sqlalchemy import create_engine, select
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy import Column, Integer, String, inspect
import re
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


class Scrape():
    def __init__(self):
        url_array = []
        page_source = ''
        success_flag = False
        # print("here")

    def scrape(self):
        url = f'https://finance.yahoo.com/quote/%5ERUI/history/?period1=723997800&period2=1729966953'
        # links_list = []
        # Selenium web driver
        options = Options() 
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0")
        driver = webdriver.Chrome(options = options)
        print("here")
        driver.get(url)
        # try:
        #     # Page Source
        page_source = driver.page_source
        # Nav Links
        parsed = []
        soup = BeautifulSoup(page_source, features="lxml")
        # Find all navigation sections
        table_sections = soup.find_all('th')
        # return table_section
        # else:
        # return None

        with open ("rui.txt", 'w') as f:
            f.write(str(table_sections))

def parse_content(file_path):
    with open (file_path, "r") as f:
        soup = BeautifulSoup(f, features="lxml")
        # Find all navigation sections
    df = pd.DataFrame()
    table_sections = soup.find_all('th', class_='yf-h2urb6')
    for item in table_sections:
        print(item.get_text())

    dict = {}
    arr = []
    column_headings = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    inner_table_sections = soup.find_all('tr')
    count = 0
    for row in inner_table_sections:
        if count > 5:
            print(arr)
            break
        else:
            inner_row_content = row.find_all('td')
            for index,inner_row in enumerate(inner_row_content):
                dict[column_headings[index]] = inner_row.get_text()
            arr.append(dict)
            count += 1
    return arr


def insert_db(array):
    engine = create_engine('sqlite:///time_series_stocks.db')
    metadata = MetaData()

    base_stock_vars = Table(
        'base_stock_vars' metadata,
        Column('Date', Date, primary_key=True)
        Column('Open', Integer),
        Column('High', Integer),
        Column('Low', Integer),
        Column('Close', Integer),
        Column('Adj Close', Integer),
        Column('Volume', Integer)
    )

file_path = "rui.txt"
x = parse_content(file_path)


# x = Scrape()
# x.scrape()

