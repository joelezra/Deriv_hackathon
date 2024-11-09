import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('risk_dashboard.db')
cursor = conn.cursor()

# Create Clients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Create Positions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    asset TEXT NOT NULL,
    position_size REAL NOT NULL,
    price REAL NOT NULL,
    pnl REAL NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close() 