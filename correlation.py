import mysql.connector
import pandas as pd

# MySQL connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=input("Password: "),
        database="mls_db"
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Function to load data from the database
def load_data(table_name):
    query = f'SELECT * FROM {table_name};'
    try:
        return pd.read_sql_query(query, db)
    except Exception as e:
        print(f"Error loading data from {table_name}: {e}")
        return pd.DataFrame()

# Function for data preprocessing
def preprocess_data(df):
    # Check data types of columns

    df = df.drop(['_Squad'], axis=1)
    # Convert numeric columns to numeric type and drop rows with missing values
    df = df.apply(pd.to_numeric, errors='coerce').dropna()


    return df

# Load data from each table
df_2018 = load_data('_2018')
df_2019 = load_data('_2019')
df_2021 = load_data('_2021')
df_2022 = load_data('_2022')

# Concatenate the DataFrames into one DataFrame
frames = [df_2018, df_2019, df_2021, df_2022]
df_combined = pd.concat(frames, ignore_index=True)

# Data Preprocessing
df_combined = preprocess_data(df_combined)

# Ensure there are numeric columns in the DataFrame
if not df_combined.empty:
    # Print columns in the DataFrame
    print("\nColumns in DataFrame:")
    print(df_combined.columns)

    # Set display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Compute and print the full correlation matrix
    correlation_matrix = df_combined.corr()
    print("\nFull Correlation Matrix:")
    print(correlation_matrix)

    # Reset display options to default
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
else:
    print("No numeric columns found in the DataFrame.")
