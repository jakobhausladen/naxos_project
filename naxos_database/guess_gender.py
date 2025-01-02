import pandas as pd
import mysql.connector
from gender_guesser.detector import Detector as GenderDetector

# Establish connection to MySQL database
database_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'naxos_db',
    'password': 'password'
}
connection = mysql.connector.connect(**database_config)
cursor = connection.cursor()

# Read names dataframe from the database
query = 'SELECT id, name FROM Person' 
df = pd.read_sql(query, connection)

# Create additional gender column using the gender_guesser package
d = GenderDetector()

def guess_gender(name):
    try:
        # Name format: LastName, FirstName1 FirstName2 etc.
        if ',' in name:
            first_names = name.split(',')[1].strip().split(' ')
            # Guess gender based on FirstName1 since GenderDetector expects a single first name
            first_name = first_names[0].strip()
            return d.get_gender(first_name)
        else:
            return 'unknown'
    except Exception as e:
        print(f'Error processing name {name}: {e}.')

df['gender'] = df['name'].apply(guess_gender)


# Create gender field for the Person table
try:
    create_field = "ALTER TABLE Person ADD COLUMN gender VARCHAR(16) DEFAULT 'unknown'"
    cursor.execute(create_field)
except mysql.connector.Error as err:
    if err.errno == 1060: # Duplicate column code
        print("Column already exists.")
    else:
        print(f"Error: {err}")

# Update Person table with gender information
update_query = "UPDATE Person SET gender = %s WHERE id = %s"
for _, row in df.iterrows():
    id = row['id']
    gender = row['gender']
    cursor.execute(update_query, (gender, id))

# Commit changes
connection.commit()

# Close connection
cursor.close()
connection.close()