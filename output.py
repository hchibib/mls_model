import mysql.connector
from prettytable import PrettyTable

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pulisic20",
    database="mls_db"
)

cursor = db.cursor()

# Fetch data from the table
cursor.execute("SELECT * FROM _2019")
data = cursor.fetchall()

# Create a PrettyTable instance
table = PrettyTable()

# Add column names to the table
table.field_names = [i[0] for i in cursor.description]

# Add data to the table
table.add_rows(data)

# Print the table
print(table)
