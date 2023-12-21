import mysql.connector
import time
from tabulate import tabulate


# python dbseeker.py -a mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro -s test -d Rfam

'''
Version alpha 0.4
 Changelog:
    - Inserted a padding limit for searching string to increase readability
    - Added argument for better parsing
    - Now user can blacklists databases to be excluded from research, OR 
        choose which database to be searched in.
        
Version alpha 0.3
 Changelog:
    - Cleaned string formatting for results
    - Printed results now display PRIMARY KEYs
        * Exexute ' python dbseeker.py -h ' to see the help message *
        
Version alpha 0.2
 Changelog:
    - Whole script rewritten using functions
    -

'''
import argparse


SEARCH_PADDING_CHARS = 25
PREPEND_APPEND_SEARCH_CHARS = "..."


def connect_to_mysql_server(host, port, user, password: str = None):
    connection = mysql.connector.connect(user=user, host=host, port=port, password=password)
    cursor = connection.cursor()
    return connection, cursor


def get_databases(cursor, fallback_databases: list[str] = None):
    if fallback_databases:
        return fallback_databases
    cursor.execute("SHOW DATABASES")
    databases = [database[0] for database in cursor.fetchall()]
    return databases


def filter_databases(databases, blacklisted_databases):
    filtered_databases = [db for db in databases if db not in blacklisted_databases]
    return filtered_databases


def row_map(row, search_term):
    _row = []

    for item in row:
        _item = str(item)
        search_begin_str = _item.lower().find(search_term.lower())
        if search_begin_str > -1:
            search_after_str = search_begin_str + len(search_term)

            item_begin_str = item_after_str = SEARCH_PADDING_CHARS

            if search_begin_str < item_begin_str:
                item_begin_str = search_begin_str

            if (len(_item) - search_after_str) < item_after_str:
                item_after_str = len(_item) - search_after_str

            padding_left = search_begin_str - item_begin_str
            padding_right = search_after_str + item_after_str

            prepend = append = ""

            if padding_left > 0:
                prepend = PREPEND_APPEND_SEARCH_CHARS

            if padding_right < len(_item):
                append = PREPEND_APPEND_SEARCH_CHARS

            _item = '\033[32m' + prepend + _item[padding_left:padding_right] + append + '\033[0m'
        else:
            if len(_item) > 5:
                _item = _item[0:5] + PREPEND_APPEND_SEARCH_CHARS
        _row.append(_item)
    return _row


def search_tables(databases, cursor, search_term):
    total_row_count = 0
    for database in databases:
        cursor.execute(f"USE `{database}`")
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        table_count = len(tables)
        if table_count == 0:
            print(f"No tables found in {database}.")
            continue
        for table_name in tables:
            try:
                cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
                columns = [column[0] for column in cursor.fetchall()]
                total_columns = len(columns)

                query = f"SELECT * FROM `{table_name}` WHERE 1=1 AND "

                for i, column_name in enumerate(columns):
                    query += f"`{column_name}` LIKE '%{search_term}%' "
                    if i + 1 < total_columns:
                        query += "OR "

                cursor.execute(query)
                rows = [row_map(list(row), search_term) for row in cursor.fetchall()]
                row_count = len(rows)

                if row_count == 0:
                    continue

                total_row_count += row_count
                print(f"Found {row_count} rows for {table_name} (DB: {database}):\n")
                print(tabulate(rows, headers=columns, tablefmt="double_grid"))

            except mysql.connector.errors.ProgrammingError as error:
                print(f"Programming Error: {error}\n")
                continue
            except Exception as error:
                print(f"General Error: {error}\n")
                continue

    return total_row_count


def main():
    parser = argparse.ArgumentParser(description="Search for a term in a database")
    parser.add_argument("-a", "--address", metavar="address", type=str, help="Enter the host address", required=True)
    parser.add_argument("-P", "--port", metavar="port", type=str, help="Enter the port", required=True)
    parser.add_argument("-u", "--user", metavar="user", type=str, help="Enter the user", required=True)
    parser.add_argument("-p", "--password", metavar="password", type=str, help="Enter the password")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--database", metavar="database", type=str, help="Enter databases you want "
                                                                              "to search in")
    group.add_argument("-bl", "--blacklist", metavar="blacklist", type=str, help="Enter databases you want"
                                                                                 " to be excluded, separated by commas")
    parser.add_argument("-s", "--search", metavar="search", type=str, help="Enter the search term", required=True)

    args = parser.parse_args()

    host = args.address
    port = args.port
    user = args.user
    password = args.password
    search_term = args.search
    user_databases = args.database
    user_blacklisted_databases = args.blacklist

    start = time.time()

    connection, cursor = connect_to_mysql_server(host, port, user, password)
    databases = get_databases(cursor, [db.strip() for db in user_databases.split(",")] if user_databases else None)

    if len(databases) == 0:
        print("No databases found.")
        exit(0)

    blacklisted_databases = ["mysql", "information_schema", "performance_schema", "sys"]

    blacklisted_databases.extend([db.strip() for db in user_blacklisted_databases.split(',')]
                                 if user_blacklisted_databases else [])

    filtered_databases = filter_databases(databases, blacklisted_databases)
    if len(filtered_databases) == 0:
        print("No databases to search on.")
        exit(0)

    print("Databases to search on:", "\n", tabulate([filtered_databases]), "\n", "searching...")

    if len(search_term) < 3:
        print("Search term should be at least 3 characters long.")
        exit(0)

    total_row_count = search_tables(filtered_databases, cursor, search_term)

    cursor.close()
    connection.close()

    end = time.time()
    time_execution = end - start
    print("Execution time:", time_execution, "seconds")
    print("Total rows found:", total_row_count)


if __name__ == "__main__":
    main()
