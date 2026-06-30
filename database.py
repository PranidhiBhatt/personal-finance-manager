import mysql.connector
from mysql.connector import Error
from config import HOST, USER, PASSWORD, DATABASE


def connect_db():
    """
    Establishes connection with MySQL database.
    Returns connection object.
    """

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        if connection.is_connected():
            print("Connected to MySQL Database.\n")

        return connection

    except Error as e:
        print("Database Connection Error:", e)
        return None
