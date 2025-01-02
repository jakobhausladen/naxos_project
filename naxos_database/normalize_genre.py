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

# Create AlbumGenre table
try:
    create_table = """
    CREATE TABLE AlbumGenre (
        catalogue_no VARCHAR(255),
        genre VARCHAR(255),
        PRIMARY KEY (catalogue_no, genre),
        FOREIGN KEY (catalogue_no) REFERENCES Album(catalogue_no)
    );
    """
    cursor.execute(create_table)
except Exception as e:
    print(f'Error: {e}')


# Get catalogue_no and genre from Album table
cursor.execute('SELECT catalogue_no, genre FROM Album')
albums = cursor.fetchall()

# Split string with genres and insert each into AlbumGenre
def normalize_genres(catalogue_no, genres):
    if genres:
        genres_list = [genre.strip() for genre in genres.split(';')]
        update_query = """
        INSERT INTO AlbumGenre (catalogue_no, genre) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE genre=VALUES(genre)
        """
        for genre in genres_list:
            cursor.execute(update_query, (catalogue_no, genre))

# Insert genres for each album
for album in albums:
    catalogue_no, genres = album
    normalize_genres(catalogue_no, genres)

# Drop original genre column from the Album table
try:
    drop_field = """
    ALTER TABLE Album
    DROP COLUMN genre
    """
    cursor.execute(drop_field)
except Exception as e:
    print(f'Error: {e}')

# Commit changes
connection.commit()

# Close connection
cursor.close()
connection.close()
