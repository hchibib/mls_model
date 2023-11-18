import mysql.connector
import csv

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pulisic20",
    database="mls_db"
)

cursor = db.cursor()


def add_wins(year):
    # Path to your CSV file
    csv_file_path = f'Playoff Wins - {year}.csv'

    # Open and read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV file
        id = 1
        for row in csv_reader:
            # Extract values from the CSV row
            csv_value = (float)(row['_Wins'])

            # Update the MySQL table with the corresponding value
            cursor.execute(f"UPDATE _{year} SET _Wins = %s WHERE id = %s", (csv_value, id))
            id += 1

years = ["2022", "2021", "2019", "2018"]
for year in years:
    add_wins(year)

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()
