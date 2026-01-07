import psycopg2


# Connect to the default postgres database

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "Kimmy027!",
    host = "localhost",
    port = "5432"
)

conn.autocommit = True
cursor = conn.cursor()

# Create a new database 
db_name = "philippines_tourism_db"
cursor.execute(f"CREATE DATABASE {db_name}")

print(f"Database {db_name} is created successfully! ")

cursor.close()

# Close out connection
conn.close()
