import sqlite3
import csv
import os

DB_FILE = "db/atlanta.db"

def create_tables(connection):
    cursor = connection.cursor()
    node_table = """
    CREATE TABLE node (
        id  INTEGER PRIMARY KEY NOT NULL,
        lat REAL,
        lon REAL,
        user TEXT,
        uid INTEGER,
        version INTEGER,
        changeset INTEGER,
        timestamp TEXT
    );
    """

    node_tags_table = """
    CREATE TABLE nodes_tags (
        id INTEGER,
        key TEXT,
        value TEXT,
        type TEXT,
        FOREIGN KEY (id) REFERENCES nodes(id)
    );
    """

    ways_table = """
    CREATE TABLE way (
        id INTEGER PRIMARY KEY NOT NULL,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
    );
    """

    ways_tags_table = """
    CREATE TABLE ways_tags (
        id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        type TEXT,
        FOREIGN KEY (id) REFERENCES ways(id)
    );
    """

    ways_nodes_table = """
    CREATE TABLE ways_nodes (
        id INTEGER NOT NULL,
        node_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES ways(id),
        FOREIGN KEY (node_id) REFERENCES nodes(id)
    );
    """

    cursor.execute(node_table)
    cursor.execute(node_tags_table)
    cursor.execute(ways_table)
    cursor.execute(ways_tags_table)
    cursor.execute(ways_nodes_table)
    connection.commit()

def insert_node(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO node (id, lat, lon, user, \
            uid, version, changeset, timestamp) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)", records)
        print('done!')
    connection.commit()

def insert_node_tag(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO nodes_tags (id, key, value, type) \
            VALUES (?, ?, ?, ?)", records)
        print('done!')
    connection.commit()

def insert_way(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO way (id, user, uid, version, \
            changeset, timestamp) \
            VALUES (?, ?, ?, ?, ?, ?)", records)
        print('done!')
    connection.commit()

def insert_way_tag(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO ways_tags (id, key, value, type) \
            VALUES (?, ?, ?, ?)", records)
        print('done!')
    connection.commit()

def insert_way_node(input_file, connection):
    cursor = connection.cursor()
    print("inserting ", input_file, "into", DB_FILE, "...")
    records = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        column = next(reader)
        records = [record for record in reader]
        cursor.executemany("INSERT INTO ways_nodes (id, node_id, position) \
            VALUES (?, ?, ?)", records)
    connection.commit()
    print('done!')

def run_query(query, connection):
    cursor = connection.cursor()
    print('executing query...')
    results = cursor.execute(query)
    connection.commit()
    print('done!')
    return results

def clear_tables(connection):
    cursor = connection.cursor()
    print('clearing tables...')
    cursor.execute('drop table if exists node')
    cursor.execute('drop table if exists node_tags')
    cursor.execute('drop table if exists way')
    cursor.execute('drop table if exists ways_tags')
    cursor.execute('drop table if exists ways_nodes')
    print('done!')
