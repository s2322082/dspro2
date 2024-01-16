import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import re
from datetime import datetime

def scrape_weather_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 気温のデータを取得
    temperature_data = []
    for row in soup.find_all('tr', class_='mtx'):
        columns = row.find_all('td')
        if len(columns) >= 3:
            date = columns[0].text.strip()
            temperature = columns[2].text.strip()
            temperature_data.append((date, temperature))

    # 降水量のデータを取得
    precipitation_data = []
    for row in soup.find_all('tr', class_='mtx'):
        columns = row.find_all('td')
        if len(columns) >= 13:
            date = columns[0].text.strip()
            precipitation = columns[12].text.strip()
            precipitation_data.append((date, precipitation))

    return temperature_data, precipitation_data

# 1つ目のURLからデータを取得
url1 = 'https://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no=44&block_no=0371&year=2023&month=12&day=&view=p1'
temperature_data1, precipitation_data1 = scrape_weather_data(url1)

# 2つ目のURLからデータを取得
url2 = 'https://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no=44&block_no=0371&year=2024&month=01&day=&view=p1'
temperature_data2, precipitation_data2 = scrape_weather_data(url2)

# 取得したデータを出力
print("1つ目のURLの気温データ:")
for date, temperature in temperature_data1:
    print(f"{date}: {temperature}℃")

print("\n1つ目のURLの降水量データ:")
for date, precipitation in precipitation_data1:
    print(f"{date}: {precipitation}mm")

print("\n2つ目のURLの気温データ:")
for date, temperature in temperature_data2:
    print(f"{date}: {temperature}℃")

print("\n2つ目のURLの降水量データ:")
for date, precipitation in precipitation_data2:
    print(f"{date}: {precipitation}mm")

    def create_database():
     with sqlite3.connect('weather_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature (
                date TEXT PRIMARY KEY,
                temperature TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rainfall (
                date TEXT PRIMARY KEY,
                pressure TEXT
            )
        ''')
def insert_data_into_database(data, table_name):
    with sqlite3.connect('weather_data.db') as conn:
        cursor = conn.cursor()
        cursor.executemany(f'INSERT OR IGNORE INTO {table_name} VALUES (?, ?)', data)
def read_data_from_database(table_name):
    with sqlite3.connect('weather_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        return cursor.fetchall()
# メインプログラム
def main():
    create_database()
    # 1つ目からデータを取得
    url1 = 'https://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no=44&block_no=0371&year=2023&month=12&day=&view=p1'
    temperature_data1, rainfall_data1 = scrape_weather_data(url1)
    insert_data_into_database(temperature_data1, 'temperature')
    insert_data_into_database(rainfall_data1, 'rainfall')
    # 2つ目からデータを取得
    url2 = 'https://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no=44&block_no=0371&year=2024&month=01&day=&view=p1'
    temperature_data2, rainfall_data2 = scrape_weather_data(url2)
    insert_data_into_database(temperature_data2, 'temperature')
    insert_data_into_database(rainfall_data2, 'rainfall')
if __name__ == "__main__":
    main()