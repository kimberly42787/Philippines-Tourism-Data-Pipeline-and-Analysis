import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="philippines_tourism_db",
    user="postgres",
    password="Kimmy027!",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Define tables
tables = [
    """
    CREATE TABLE IF NOT EXISTS countries_list (
        country_id SERIAL PRIMARY KEY,
        country VARCHAR(100) UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS monthly_visitors (
        monthly_id SERIAL PRIMARY KEY,
        country_id INT REFERENCES countries_list(country_id),
        year INT,
        month VARCHAR(20),
        visitors BIGINT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS yearly_visitors (
        yearly_id SERIAL PRIMARY KEY, 
        country_id INT REFERENCES countries_list(country_id),
        year INT, 
        total_visitors BIGINT,
        percentage FLOAT, 
        previous_year_total BIGINT,
        growth_rate FLOAT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS special_categories (
        id SERIAL PRIMARY KEY,
        category VARCHAR(50), 
        year INT,
        month VARCHAR(20),
        visitors BIGINT
    );
    """
]

# Execute table creation
for table in tables:
    cur.execute(table)

conn.commit()
print("Tables created successfully!")

cur.close()
conn.close()