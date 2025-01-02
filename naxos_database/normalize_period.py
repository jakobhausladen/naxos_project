import mysql.connector

# Establish connection to the database
database_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'naxos_db'
}
connection = mysql.connector.connect(**database_config)
cursor = connection.cursor()

# Create AlbumPeriod table
try:
    create_table = """
    CREATE TABLE AlbumPeriod (
        catalogue_no VARCHAR(255),
        period VARCHAR(255),
        PRIMARY KEY (catalogue_no, period),
        FOREIGN KEY (catalogue_no) REFERENCES Album(catalogue_no)
    );
    """
    cursor.execute(create_table)
except Exception as e:
    print(f'Error: {e}')


# Get catalogue_no and genre from Album table
cursor.execute('SELECT catalogue_no, period FROM Album')
albums = cursor.fetchall()

# Split string with periods and insert each into AlbumPeriod
def normalize_periods(catalogue_no, periods):
    if periods:
        period_list = [period.strip() for period in periods.split(';')]
        update_query = """
        INSERT INTO AlbumPeriod (catalogue_no, period) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE period=VALUES(period)
        """
        for period in period_list:
            cursor.execute(update_query, (catalogue_no, period))

# Insert periods for each album
for album in albums:
    catalogue_no, periods = album
    normalize_periods(catalogue_no, periods)

# Drop original period column from the Album table
try:
    drop_field = """
    ALTER TABLE Album
    DROP COLUMN period
    """
    cursor.execute(drop_field)
except Exception as e:
    print(f'Error: {e}')

# Commit changes
connection.commit()

# Close connection
cursor.close()
connection.close()
