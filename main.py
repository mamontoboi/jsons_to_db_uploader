import os
import psycopg2
import json
import logging

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def json_postgres(folder):
    """Servers for import of json files into db"""
    conn = psycopg2.connect(
        host="localhost",
        database="json_base",
        user="postgres",
        password="postgres"
    )

    # Create necessary tables if they don't exist
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS json_table (
                id SERIAL PRIMARY KEY,
                data jsonb
            );
        """)

    # Traverse through folder structure and extract data from JSON files
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    data = json.load(f)

                # Check if data already exists in database
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM json_table WHERE data = %s", (json.dumps(data),))
                    result = cur.fetchone()

                if result is not None:
                    # Data already exists in database, skip file
                    logging.info(f"Already in database: {file_path}")
                else:
                    # Data not in database, insert into table
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO json_table (data) VALUES (%s)", (json.dumps(data),))
                    conn.commit()
                    logging.info(f"Imported into database: {file_path}")


if __name__ == '__main__':
    folder_path = input("Write the path to the folder: ")
    json_postgres(folder_path)
