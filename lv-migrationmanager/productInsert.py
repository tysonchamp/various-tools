import csv
import mysql.connector
import re

CSV_FILE = 'products.csv'
TABLE_NAME = 'products'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'crosdeal'
}

def slugify(value):
    value = value.lower()
    value = re.sub(r'[^a-z0-9\s-]', '', value)
    value = re.sub(r'[\s\-]+', '-', value)
    return value.strip('-')

def create_table(cursor, headers):
    columns = []
    for h in headers:
        columns.append(f"`{h}` TEXT")
    columns_sql = ', '.join(columns)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({columns_sql})")

def insert_row(cursor, headers, row):
    placeholders = ','.join(['%s'] * len(headers))
    columns = ','.join(f"`{h}`" for h in headers)
    values = [None if v == 'NULL' else v for v in row]
    cursor.execute(
        f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})",
        values
    )

def main():
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        orig_headers = next(reader)
        # Insert 'slug' after 'name'
        headers = []
        for h in orig_headers:
            headers.append(h)
            if h == 'name':
                headers.append('slug')
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        create_table(cur, headers)
        for row in reader:
            # Insert slug after name
            new_row = []
            for idx, val in enumerate(row):
                new_row.append(val)
                if orig_headers[idx] == 'name':
                    new_row.append(slugify(val))
            insert_row(cur, headers, new_row)
        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserted all rows from {CSV_FILE} into MySQL database '{DB_CONFIG['database']}'")

if __name__ == '__main__':
    main()
