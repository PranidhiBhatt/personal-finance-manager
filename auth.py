from database import connect_db
from getpass import getpass


class AuthManager:

    def __init__(self):
        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Could not connect to database.")

        self.cursor = self.connection.cursor()

    # ===============================
    # LOGIN
    # ===============================

    def login(self):

        print("\n========== LOGIN ==========\n")

        email = input("Email: ")

        password = getpass("Password: ")

        sql = """
        SELECT user_id, name
        FROM Users
        WHERE email=%s AND password=%s
        """

        self.cursor.execute(sql, (email, password))

        user = self.cursor.fetchone()

        if user:

            print(f"\nWelcome, {user[1]}!\n")

            return {
                "user_id": user[0],
                "name": user[1]
            }

        print("\nInvalid Email or Password.\n")

        return None

    # ===============================
    # CLOSE CONNECTION
    # ===============================

    def close_connection(self):

        if self.connection.is_connected():

            self.cursor.close()

            self.connection.close()
