from database import connect_db
from models import Income
from datetime import datetime

class IncomeManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()

# ==========================================
# SOURCE
# ==========================================

    def validate_source(self):

        while True:

            source = input("Income Source: ").strip()

            if source != "":
                return source

            print("Income Source cannot be empty.")

# ==========================================
# AMOUNT
# ==========================================

    def validate_amount(self):

        while True:

            try:

                amount = float(input("Amount (₹): "))

                if amount > 0:
                    return amount

                print("Amount must be greater than zero.")

            except ValueError:

                print("Enter a valid amount.")
# ==========================================
# ADD INCOME
# ==========================================

    def add_income(self):

        print("\n" + "=" * 50)
        print("ADD INCOME")
        print("=" * 50)

        # Logged-in user's ID
        user_id = self.user["user_id"]

        # Get income details
        source = self.validate_source()
        amount = self.validate_amount()

        # Automatically get current date and time
        income_date = datetime.now()

        # Create Income object
        income = Income(
            source,
            amount,
            income_date,
            user_id
        )

        sql = """
        INSERT INTO Income
        (user_id, source, amount, income_date)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            income.user_id,
            income.source,
            income.amount,
            income.income_date
        )

        try:

            self.cursor.execute(sql, values)

            self.connection.commit()

            print("\nIncome added successfully!")

        except Exception as e:

            print("\nError:", e)

# ==========================================
# SHOW INCOME
# ==========================================

    def show_income(self):

        sql = """
        SELECT
            income_id,
            source,
            amount,
            income_date
        FROM Income
        WHERE user_id = %s
        ORDER BY income_date DESC
        """

        try:

            self.cursor.execute(sql, (self.user["user_id"],))

            incomes = self.cursor.fetchall()

            if not incomes:
                print("\nNo income records found.\n")
                return

            print("\n" + "=" * 80)
            print(f"Income Records for {self.user['name']}")
            print("=" * 80)

            print(
                f"{'ID':<5}"
                f"{'Source':<25}"
                f"{'Amount':<15}"
                f"{'Date & Time'}"
            )

            print("-" * 80)

            for income in incomes:

                formatted_date = income[3].strftime("%d-%b-%Y %I:%M %p")

                print(
                    f"{income[0]:<5}"
                    f"{income[1]:<25}"
                    f"₹{income[2]:<13.2f}"
                    f"{formatted_date}"
                )

            print()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # UPDATE INCOME
    # ==========================================

    def update_income(self):

        self.show_income()

        try:

            income_id = int(input("\nEnter Income ID to update: "))

        except ValueError:

            print("Invalid Income ID.")
            return

        sql = """
        SELECT income_id
        FROM Income
        WHERE income_id = %s
        AND user_id = %s
        """

        self.cursor.execute(sql, (income_id, self.user["user_id"]))

        if self.cursor.fetchone() is None:

            print("\nIncome record not found.")
            return

        print("\nLeave a field blank to keep the current value.\n")

        source = input("New Source: ").strip()
        amount = input("New Amount: ").strip()

        updates = []
        values = []

        if source:

            updates.append("source = %s")
            values.append(source)

        if amount:

            try:

                amount = float(amount)

                if amount <= 0:

                    print("Amount must be greater than zero.")
                    return

                updates.append("amount = %s")
                values.append(amount)

            except ValueError:

                print("Invalid amount.")
                return

        if not updates:

            print("\nNothing to update.")
            return

        sql = f"""
        UPDATE Income
        SET {', '.join(updates)}
        WHERE income_id = %s
        """

        values.append(income_id)

        try:

            self.cursor.execute(sql, tuple(values))

            self.connection.commit()

            print("\nIncome updated successfully!")

        except Exception as e:

            print("\nError:", e)


    # ==========================================
    # DELETE INCOME
    # ==========================================

    def delete_income(self):

        self.show_income()

        try:

            income_id = int(input("\nEnter Income ID to delete: "))

        except ValueError:

            print("Invalid Income ID.")
            return

        sql = """
        SELECT income_id
        FROM Income
        WHERE income_id = %s
        AND user_id = %s
        """

        self.cursor.execute(sql, (income_id, self.user["user_id"]))

        if self.cursor.fetchone() is None:

            print("\nIncome record not found.")
            return

        confirm = input("Are you sure? (y/n): ").lower()

        if confirm != "y":

            print("\nDeletion cancelled.")
            return

        sql = """
        DELETE FROM Income
        WHERE income_id = %s
        """

        try:

            self.cursor.execute(sql, (income_id,))

            self.connection.commit()

            print("\nIncome deleted successfully!")

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # TOTAL INCOME
    # ==========================================

    def total_income(self):

        sql = """
        SELECT SUM(amount)
        FROM Income
        WHERE user_id = %s
        """

        try:

            self.cursor.execute(sql, (self.user["user_id"],))

            total = self.cursor.fetchone()[0]

            if total is None:

                total = 0

            print("\n" + "=" * 40)
            print(f"Total Income : ₹{total:.2f}")
            print("=" * 40)

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # CLOSE CONNECTION
    # ==========================================

    def close_connection(self):

        if self.connection.is_connected():

            self.cursor.close()

            self.connection.close()

            print("\nDatabase connection closed.")

