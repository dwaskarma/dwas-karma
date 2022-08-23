import csv
import sqlite3

DB_NAME = "users.db"
FILE_NAME = "sample_users.csv"

USER_INPUT = """
Enter the option: 
    1. CREATE TABLE users
    2. Import data from CSV file
    3. Select all records from user.
    4. Delete a record from table user.
    5. Delete all records from table
    6. Update a record with id.
    7. Insert records manually to table.
"""

CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name CHAR(255) NOT NULL,
        last_name CHAR(255) NOT NULL,
        company_name CHAR(255) NOT NULL,
        address CHAR(255) NOT NULL,
        city CHAR(255) NOT NULL,
        county CHAR(255) NOT NULL,
        state CHAR(255) NOT NULL,
        zip REAL NOT NULL,
        phone1 CHAR(255) NOT NULL,
        phone2 CHAR(255),
        email CHAR(255) NOT NULL,
        web text
    );
"""
COLUMNS = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)

COLUMN_INPUT_STRING = f"""
Which column would you like to update?. Please make sure column is one of the following:
{COLUMNS} 
"""


def create_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def create_table_user(conn):
    cur = conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User table created successfully.")


def open_csv_file(file_name):
    db_data = []

    with open(file_name) as f:
        data = csv.reader(f)  # iterator
        for datum in data:
            db_data.append(tuple(datum))

    return db_data


def insert_records_to_table(conn, data):
    insert_query = """
    INSERT INTO 
        users
            (first_name, last_name, company_name, address, city, county, state, zip, phone1, phone2, email, web)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    
    """
    cur = conn.executemany(insert_query, data)
    conn.commit()
    print("All records were inserted to table.")


def select_records_from_table(conn):
    cur = conn.execute("SELECT * from users;")
    for row in cur:
        print(row)


def delete_record(conn, user_id):
    cur = conn.execute("DELETE from users where id = ?", (user_id,))
    conn.commit()
    print(f"Successfully delete record with id {user_id}")


def delete_all_records(conn):
    cur = conn.execute("DELETE from users;")
    conn.commit()
    print("All records were successfully deleted.")


def update_record_with_id(conn, column_name, column_value, user_id):
    cur = conn.execute(
        f"UPDATE users set {column_name} = ? where id = ?",
        (column_value, user_id),
    )
    conn.commit()
    print(
        f"Successfully updated {column_name} of user {user_id} with value {column_value}"
    )


def main():
    conn = create_connection(DB_NAME)

    while True:

        user_input = input(USER_INPUT)

        if user_input == "1":
            create_table_user(conn)

        elif user_input == "2":
            data = open_csv_file(FILE_NAME)
            insert_records_to_table(conn, data)

        elif user_input == "3":
            select_records_from_table(conn)

        elif user_input == "4":
            record_id = input("Enter id of record: ")
            if record_id.isnumeric():
                delete_record(conn, record_id)

        elif user_input == "5":
            confirmation = input(
                "Are you sure? \
    Press y or Yes to continue. \
    or press n or no to skip."
            )
            if confirmation.lower() in ["y", "yes"]:
                delete_all_records(conn)

        elif user_input == "6":
            column_name = input(COLUMN_INPUT_STRING)
            if column_name in COLUMNS:
                column_value = input(f"Enter the value of {column_name}: ")
                user_id = input("Enter the id of user: ")
                update_record_with_id(
                    conn,
                    column_name,
                    column_value,
                    user_id,
                )

        elif user_input == '7':
            data=[]
            for column  in COLUMNS:
                column_data =input (f'Enter{column}')
                data.append (column_data)
            data = [tuple(data)]
            insert_records_to_table(conn,data)

        else:
            exit()

if __name__ == "__main__":
    main()
