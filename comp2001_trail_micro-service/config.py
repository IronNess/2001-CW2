import pyodbc

def get_db_connection():
    server = 'DIST-6-505.uopnet.plymouth.ac.uk'
    database = 'COMP2001_VRadmore'
    username = 'VRadmore'
    password = 'Lc1M674*'
    driver = '{ODBC Driver 18 for SQL Server}'

    conn_str = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'Encrypt=Yes;'
        'TrustServerCertificate=Yes;'
        'Connection Timeout=30;'
    )
    return pyodbc.connect(conn_str)

