import requests
from bs4 import BeautifulSoup
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=input("Password: ")
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS mls_db")
cursor.execute("USE mls_db")

def create_table(headers, year):
    # Create a table to store the scraped data
    cursor.execute(f"DROP TABLE IF EXISTS {year}")
    query = f"CREATE TABLE IF NOT EXISTS {year} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join([f'{header} VARCHAR(255)' for header in headers])})"
    cursor.execute(query)



def scrape_fbref_data(url, year):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the data
        table = soup.find('table', {'id': 'stats_squads_standard_for'})

        # Check if the table is found
        if table:
            # Extract rows from the table
            rows = table.find_all('tr')

            # Process and print the header row
            header_row = rows[1]
            headers = ['_' + header['aria-label'].replace(' ', '_').replace('#', 'Num').replace('+', 'Plus').replace('-', '_').replace(':', '').replace('/', '_per_') for header in header_row.find_all('th')]
            headers[-1] = '_npxG_Plus_xAG_per_90'

            create_table(headers, year)


            # Process and print the data rows
            for row in rows[2:]:
                datah = [th.text.strip() for th in row.find_all('th')]
                datad = [(float)(td.text.strip().replace(',', '')) for td in row.find_all('td')]
                data = datah + datad

                cursor.execute(f"INSERT INTO {year} VALUES (NULL, {', '.join(['%s' for _ in data])})", data)


            db.commit()

        else:
            print("Table not found on the page.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    urls = ["https://fbref.com/en/comps/22/Major-League-Soccer-Stats", "https://fbref.com/en/comps/22/2022/2022-Major-League-Soccer-Stats", "https://fbref.com/en/comps/22/2021/2021-Major-League-Soccer-Stats", "https://fbref.com/en/comps/22/2019/2019-Major-League-Soccer-Stats", "https://fbref.com/en/comps/22/2018/2018-Major-League-Soccer-Stats"]
    scrape_fbref_data(urls[0], "_2023")
    scrape_fbref_data(urls[1], "_2022")
    scrape_fbref_data(urls[2], "_2021")
    scrape_fbref_data(urls[3], "_2019")
    scrape_fbref_data(urls[4], "_2018")
