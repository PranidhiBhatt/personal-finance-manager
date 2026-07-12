from database import connect_db

class AuthManager:

    def __init__(self):
        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Could not connect to database.")

        self.cursor = self.connection.cursor()

    # ===============================
    # VALIDATE NAME
    # ===============================

    def validate_name(self, name):

        name = name.strip()

        if not name:

            return False, "Name cannot be empty."

        if len(name) < 3:

            return False, "Name must contain at least 3 characters."

        return True, ""

    # ===============================
    # VALIDATE EMAIL
    # ===============================

    def validate_email(self, email):

        email = email.strip()

        if not email:

            return False, "Email cannot be empty."

        if "@" not in email or "." not in email:

            return False, "Please enter a valid email."

        return True, ""

    # ===============================
    # VALIDATE PASSWORD
    # ===============================

    def validate_password(self, password):

        if not password:

            return False, "Password cannot be empty."

        if len(password) < 6:

            return False, "Password must contain at least 6 characters."

        return True, ""

    # ===============================
    # CHECK EMAIL
    # ===============================

    def email_exists(self, email):

        sql = """
        SELECT user_id
        FROM Users
        WHERE email = %s
        """

        self.cursor.execute(
            sql,
            (email,)
        )

        return self.cursor.fetchone() is not None

    # ===============================
    # REGISTER
    # ===============================

    def register(
        self,
        name,
        email,
        password,
        confirm_password
    ):

        valid, message = self.validate_name(name)

        if not valid:

            return False, message

        valid, message = self.validate_email(email)

        if not valid:

            return False, message

        valid, message = self.validate_password(password)

        if not valid:

            return False, message

        if password != confirm_password:

            return False, "Passwords do not match."

        if self.email_exists(email):

            return False, "Email already exists."

        sql = """
        INSERT INTO Users
        (
            name,
            email,
            password
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """

        values = (
            name,
            email,
            password
        )

        try:

            self.cursor.execute(
                sql,
                values
            )

            self.connection.commit()

            return True, "Account created successfully."

        except Exception as e:

            return False, str(e)

    # ===============================
    # LOGIN
    # ===============================

    def login(self, email, password):

        sql = """
        SELECT user_id, name, email
        FROM Users
        WHERE email=%s AND password=%s
        """

        self.cursor.execute(sql, (email, password))

        user = self.cursor.fetchone()

        if user:

            return {
                "user_id": user[0],
                "name": user[1],
                "email": user[2]
            }

        return None

    # ===============================
    # CLOSE CONNECTION
    # ===============================

    def close_connection(self):

        if self.connection.is_connected():

            self.cursor.close()

            self.connection.close()
