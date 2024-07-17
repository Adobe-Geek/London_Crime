import json
import psycopg2
from psycopg2.extras import execute_values

# postgreSQL connection details
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "123"
DB_HOST = "localhost"
DB_PORT = "5432"


def load_data_to_postgres(json_filename, table_name):
    # read data from JSON file
    with open(json_filename, "r") as json_file:
        data = json.load(json_file)

    # connect to database
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()

    # create table if not exists
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        reported_by TEXT,
        falls_within TEXT,
        longitude DOUBLE PRECISION,
        latitude DOUBLE PRECISION,
        location TEXT,
        crime_type TEXT,
        last_outcome_category TEXT,
        date TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    # prepare data for insertion
    values = [
        (
            record.get("Reported by"),
            record.get("Falls within"),
            record.get("Longitude"),
            record.get("Latitude"),
            record.get("Location"),
            record.get("Crime type"),
            record.get("Last outcome category"),
            record.get("Date"),
        )
        for record in data
    ]

    # insert data
    insert_query = f"""
    INSERT INTO {table_name} (
        reported_by,
        falls_within,
        longitude,
        latitude,
        location,
        crime_type,
        last_outcome_category,
        date
    ) VALUES %s
    ON CONFLICT DO NOTHING;
    """
    execute_values(cursor, insert_query, values)
    conn.commit()

    # close the connection
    cursor.close()
    conn.close()
    print(f"Data loaded into PostgreSQL table {table_name}")


def main():
    years = [2022, 2023, 2024]
    for year in years:
        json_filename = f"london_crime_data_{year}_{4:02d}.json"
        table_name = f"london_crime_data_{year}"
        try:
            load_data_to_postgres(json_filename, table_name)
        except FileNotFoundError:
            print(f"File {json_filename} not found. Skipping...")


if __name__ == "__main__":
    main()
