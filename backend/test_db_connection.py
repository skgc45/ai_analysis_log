import mysql.connector


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="mysql_db", user="testuser", password="testpassword", database="testdb"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed")


if __name__ == "__main__":
    connect_to_database()
