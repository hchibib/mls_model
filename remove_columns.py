import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=input("Password: "),
    database="mls_db"
)

cursor = db.cursor()


def remove_columns(year):
    cursor.execute(f"ALTER TABLE {year} DROP COLUMN _Matches_Played, DROP COLUMN _Starts, DROP COLUMN _Minutes, DROP COLUMN _90s_Played;")


years = ["_2023", "_2022", "_2021", "_2019", "_2018"]
for year in years:
    remove_columns(year)

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()