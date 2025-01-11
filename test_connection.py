import pyodbc

# Connection parameters
server = 'socem1.uopnet.plymouth.ac.uk'  # SQL Server host
database = 'COMP2001_VRadmore'           # Your database name
username = 'VRadmore'                    # Your username
password = 'LclM674*'                    # Your password
driver = '{ODBC Driver 18 for SQL Server}'  # SQL Server ODBC driver

# Connection string
conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No'
)

try:
    conn = pyodbc.connect(conn_str)
    print("Database connection successful!")
    conn.close()
except pyodbc.Error as e:
    print(f"Database connection failed: {e}")