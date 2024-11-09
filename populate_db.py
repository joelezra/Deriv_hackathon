import requests
import sqlite3
import pandas as pd

def setup_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('risk_dashboard.db')
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS clients")
    cursor.execute("DROP TABLE IF EXISTS positions")

    # Create new tables
    cursor.execute("""
    CREATE TABLE clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        asset TEXT,
        position_size REAL,
        purchase_price REAL,
        pnl REAL,
        current_price REAL,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    # Commit and close the database connection
    conn.commit()
    conn.close()

def fetch_transactions(api_url):
    try:
        response = requests.get(api_url)
        data = response.json()
    except ValueError as e:
        print("Error parsing JSON:", e)
        return []

    # Extract the list of transactions
    transactions = data.get('transactions', [])
    return transactions

def insert_data_into_db(transactions):
    # Connect to the SQLite database
    conn = sqlite3.connect('risk_dashboard.db')
    cursor = conn.cursor()

    # Extract user_id from the transactions
    user_ids = set(item['user_id'] for item in transactions if 'user_id' in item)

    # Insert user_ids into the clients table
    clients = [(user_id,) for user_id in user_ids]
    cursor.executemany('INSERT OR IGNORE INTO clients (name) VALUES (?)', clients)

    # Extract and insert positions data
    positions = []
    for item in transactions:
        client_id = int(item['user_id'])  # Assuming user_id corresponds to client_id
        asset = item['symbol']
        position_size = item['units']
        price = item['purchase_price']
        pnl = item['p_l']
        
        # Assuming you have a way to fetch current prices
        current_price = fetch_current_price(asset)
        
        positions.append((client_id, asset, position_size, price, pnl, current_price))

    cursor.executemany('INSERT INTO positions (client_id, asset, position_size, purchase_price, pnl, current_price) VALUES (?, ?, ?, ?, ?, ?)', positions)

    # Commit and close the database connection
    conn.commit()
    conn.close()

def fetch_current_price(asset):
    # Define the API endpoint
    api_url = 'http://167.99.116.224:8000/crypto_real_time'  # Replace with the actual API URL

    try:
        # Make a GET request to the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        # Find the current price for the specified asset
        for crypto in data.get('crypto', []):
            if crypto['symbol'] == asset:
                return crypto['price']
        # If the asset is not found, return None or handle accordingly
        print(f"Asset {asset} not found in the crypto data.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching current price for {asset}: {e}")
        return None

def calculate_aggregate_exposure():
    # Connect to the SQLite database
    conn = sqlite3.connect('risk_dashboard.db')
    cursor = conn.cursor()

    # Fetch positions data from the database
    query = """
    SELECT client_id, asset, position_size, current_price
    FROM positions
    """
    positions_df = pd.read_sql_query(query, conn)

    current_price = fetch_current_price(positions_df['asset'][0])
    # Calculate exposure for each position
    positions_df['exposure'] = positions_df['position_size'] * current_price

    # Aggregate exposure by asset
    aggregate_exposure = positions_df.groupby('asset')['exposure'].sum().reset_index()

    # Display the aggregate exposure
    print("Aggregate Exposure by Asset:")
    print(aggregate_exposure)

    # Close the database connection
    conn.close()

# Example usage
setup_database()
api_url = 'http://tayar.pro:8000/transactions'
transactions = fetch_transactions(api_url)
insert_data_into_db(transactions)
calculate_aggregate_exposure() 