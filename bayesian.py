import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.metrics import mean_squared_error


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
    # Check if '_Wins' column exists in the DataFrame
    if '_Wins' in df.columns:
        # Example: Handling missing values by dropping rows
        df = df.dropna(subset=['_Wins'])
        return df
    else:
        return df

# Function to train and evaluate the model
def train_and_evaluate_model(X_train, y_train, X_test, y_test, model_type='linear'):
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'bayesian':
        model = BayesianRidge()
    else:
        raise ValueError("Invalid model_type. Use 'linear' or 'bayesian'.")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    return model

# ... (Rest of the code remains unchanged)
# Function to make predictions on new data
def make_predictions(model, df_new):
    # Create a placeholder for _Wins column
    df_new['_Wins'] = None

    # Extract features
    X_new = df_new.drop(['_Wins', '_Squad', 'id'], axis=1)

    # Make predictions
    y_pred_new = model.predict(X_new)

    # Assign predicted values to the _Wins column
    df_new['_Wins'] = y_pred_new

    return df_new


# Main script
if __name__ == "__main__":
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



    # Split Data
    X = df_combined.drop(['_Wins', '_Squad', 'id'], axis=1)
    y = df_combined['_Wins']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and Evaluate the Linear Regression Model
    trained_linear_model = train_and_evaluate_model(X_train, y_train, X_test, y_test, model_type='linear')

    # Train and Evaluate the Bayesian Ridge Model
    trained_bayesian_model = train_and_evaluate_model(X_train, y_train, X_test, y_test, model_type='bayesian')

    # Make Predictions on New Data
    df_new = load_data('_2023')  # Replace with the actual name of your new table
    df_new_processed = preprocess_data(df_new)

    # Make Predictions using Linear Regression Model
    df_linear_predictions = make_predictions(trained_linear_model, df_new_processed)
    print("Linear Regression Model Predictions:")
    print(df_linear_predictions[['_Squad', '_Wins']])

    # Make Predictions using Bayesian Ridge Model
    df_bayesian_predictions = make_predictions(trained_bayesian_model, df_new_processed)
    print("\nBayesian Ridge Model Predictions:")
    print(df_bayesian_predictions[['_Squad', '_Wins']])
