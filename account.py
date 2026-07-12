from database import connect_db

class AccountManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()

    # ==========================================
    # LOAD PROFILE
    # ==========================================

    def load_profile(self):

        sql = """
        SELECT
            name,
            email
        FROM Users
        WHERE user_id = %s
        """

        self.cursor.execute(
            sql,
            (self.user["user_id"],)
        )

        return self.cursor.fetchone()

    # ==========================================
    # VALIDATE NAME
    # ==========================================

    def validate_name(self, name):

        name = name.strip()

        if not name:

            return False, "Name cannot be empty."

        if len(name) < 3:

            return False, "Name must contain at least 3 characters."

        return True, ""

    # ==========================================
    # VALIDATE EMAIL
    # ==========================================

    def validate_email(self, email):

        email = email.strip()

        if not email:

            return False, "Email cannot be empty."

        if "@" not in email or "." not in email:

            return False, "Please enter a valid email."

        return True, ""

    # ==========================================
    # CHECK EMAIL
    # ==========================================

    def email_exists(self, email):

        sql = """
        SELECT user_id
        FROM Users
        WHERE email = %s
        AND user_id != %s
        """

        self.cursor.execute(
            sql,
            (
                email,
                self.user["user_id"]
            )
        )

        return self.cursor.fetchone() is not None

    # ==========================================
    # UPDATE PROFILE
    # ==========================================

    def update_profile(self, name, email):

        # Validate Name
        valid, message = self.validate_name(name)

        if not valid:

            return False, message

        # Validate Email
        valid, message = self.validate_email(email)

        if not valid:

            return False, message

        # Check Duplicate Email
        if self.email_exists(email):

            return False, "Email already exists."

        sql = """
        UPDATE Users
        SET
            name = %s,
            email = %s
        WHERE user_id = %s
        """

        values = (
            name,
            email,
            self.user["user_id"]
        )

        try:

            self.cursor.execute(
                sql,
                values
            )

            self.connection.commit()

            # Update the logged-in user's information
            self.user["name"] = name
            self.user["email"] = email

            return True, "Profile updated successfully."

        except Exception as e:

            return False, str(e)
