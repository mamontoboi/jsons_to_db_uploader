The Python script goes through a given folder and its subfolders, extracts data from JSON files, and imports it into a PostgreSQL database. If the data already exists in the database, the script recognizes it and ignores it. The logging feature is implemented to maintain the import history.

The script assumes that the database username and password are both "postgres".

To run the script on Windows:
- `pip install -r requirements.txt`
- `python main.py`
