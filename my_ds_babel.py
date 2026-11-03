
import sqlite3
import csv
from io import StringIO


def sql_to_csv(database, table_name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    column_names = [
        description[0] for description in cursor.description
    ]

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(column_names)
    writer.writerows(rows)

    final_string = output.getvalue()

    conn.close()

    return final_string


def csv_to_sql(csv_content, database, table_name):

    reader = csv.reader(csv_content)

    column_names = next(reader)

    column_definitions = [
        f'"{column}" TEXT' for column in column_names
    ]

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    columns = ", ".join(column_definitions)

    create_table_sql = f"""
    CREATE TABLE {table_name} (
        {columns}
    )
    """

    cursor.execute(create_table_sql)

    placeholders = ", ".join(
        ["?"] * len(column_names)
    )

    insert_sql = f"""
    INSERT INTO {table_name}
    VALUES ({placeholders})
    """

    rows = []

    for values in reader:
        rows.append(values)

    cursor.executemany(insert_sql, rows)

    conn.commit()
    conn.close()
