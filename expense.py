from database import connect_db
from models import Expense
from datetime import datetime

class ExpenseManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()

    # ==========================================
    # CATEGORY MENU
    # ==========================================

    def choose_category(self):

        categories = [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Medical",
            "Travel",
            "Education",
            "Other"
        ]

        print("\nChoose Category\n")

        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        while True:

            try:

                choice = int(input("\nEnter Choice: "))

                if 1 <= choice <= len(categories):
                    return categories[choice - 1]

                print("Invalid choice.")

            except ValueError:
                print("Enter a valid number.")
    # ==========================================
    # EXPENSE TYPE
    # ==========================================

    def validate_expense_type(self):

        while True:

            expense_type = input("Expense Type: ").strip()

            if expense_type != "":
                return expense_type

            print("Expense Type cannot be empty.")
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
    # DESCRIPTION
    # ==========================================

    def validate_description(self):

        description = input("Description: ").strip()

        if description == "":
            return "No Description"

        return description

    # ==========================================
    # ADD EXPENSE DATA
    # ==========================================

    def add_expense_data(
        self,
        expense_type,
        category,
        amount,
        description,
        expense_date,
        user_id
    ):

        expense = Expense(
            expense_type,
            category,
            amount,
            expense_date,
            description,
            user_id
        )

        sql = """
        INSERT INTO Expenses
        (user_id, expense_name, category, amount, expense_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            expense.user_id,
            expense.expense_type,
            expense.category,
            expense.amount,
            expense.expense_date,
            expense.description
        )

        try:

            self.cursor.execute(sql, values)

            self.connection.commit()

            return True

        except Exception as e:

            print("\nError:", e)

            return False
    # ==========================================
    # ADD EXPENSE
    # ==========================================

    def add_expense(self):

        print("\n" + "=" * 50)
        print("ADD EXPENSE")
        print("=" * 50)

        user_id = self.user["user_id"]

        expense_type = self.validate_expense_type()
        category = self.choose_category()
        amount = self.validate_amount()
        description = self.validate_description()

        expense_date = datetime.now()

        success = self.add_expense_data(
            expense_type,
            category,
            amount,
            description,
            expense_date,
            user_id
        )

        if success:

            print("\nExpense added successfully!")
    # ==========================================
    # SHOW EXPENSES
    # ==========================================

    def show_expenses(self):

        sql = """
        SELECT
            expense_id,
            expense_name,
            category,
            amount,
            expense_date,
            description
        FROM Expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC
        """

        try:
            self.cursor.execute(sql, (self.user["user_id"],))
            expenses = self.cursor.fetchall()

            if not expenses:
                print("\nNo expenses found.\n")
                return

            print("\n" + "=" * 100)
            print(f"Expenses for {self.user['name']}")
            print("=" * 100)

            print(
                f"{'ID':<5}"
                f"{'Expense Type':<20}"
                f"{'Category':<15}"
                f"{'Amount':<12}"
                f"{'Date & Time':<22}"
                f"Description"
            )

            print("-" * 100)

            for expense in expenses:

                formatted_date = expense[4].strftime("%d-%b-%Y %I:%M %p")

                print(
                    f"{expense[0]:<5}"
                    f"{expense[1]:<20}"
                    f"{expense[2]:<15}"
                    f"₹{expense[3]:<10.2f}"
                    f"{formatted_date:<22}"
                    f"{expense[5]}"
                )

            print()

        except Exception as e:
            print("\nError:", e)
    # ==========================================
    # UPDATE EXPENSE
    # ==========================================

    def update_expense(self):

        # Show user's expenses first
        self.show_expenses()

        try:
            expense_id = int(input("\nEnter Expense ID to update: "))

        except ValueError:
            print("Invalid Expense ID.")
            return

        # Check if the expense belongs to the logged-in user
        sql = """
        SELECT expense_id
        FROM Expenses
        WHERE expense_id = %s
        AND user_id = %s
        """

        self.cursor.execute(sql, (expense_id, self.user["user_id"]))

        if self.cursor.fetchone() is None:
            print("\nExpense not found.")
            return

        print("\nLeave a field blank to keep the current value.\n")

        expense_type = input("New Expense Type: ").strip()
        amount = input("New Amount: ").strip()
        description = input("New Description: ").strip()

        # Build the UPDATE query dynamically
        updates = []
        values = []

        if expense_type:
            updates.append("expense_name = %s")
            values.append(expense_type)

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

        if description:
            updates.append("description = %s")
            values.append(description)

        if not updates:
            print("\nNothing to update.")
            return

        sql = f"""
        UPDATE Expenses
        SET {', '.join(updates)}
        WHERE expense_id = %s
        """

        values.append(expense_id)

        try:
            self.cursor.execute(sql, tuple(values))
            self.connection.commit()

            print("\nExpense updated successfully!")

        except Exception as e:
            print("\nError:", e)
    # ==========================================
    # DELETE EXPENSE
    # ==========================================

    def delete_expense(self):

        # Show current expenses
        self.show_expenses()

        try:
            expense_id = int(input("\nEnter Expense ID to delete: "))

        except ValueError:
            print("Invalid Expense ID.")
            return

        # Check if expense belongs to logged-in user
        sql = """
        SELECT expense_id
        FROM Expenses
        WHERE expense_id = %s
        AND user_id = %s
        """

        self.cursor.execute(sql, (expense_id, self.user["user_id"]))

        if self.cursor.fetchone() is None:
            print("\nExpense not found.")
            return

        confirm = input("Are you sure you want to delete this expense? (y/n): ").lower()

        if confirm != "y":
            print("\nDeletion cancelled.")
            return

        sql = """
        DELETE FROM Expenses
        WHERE expense_id = %s
        """

        try:
            self.cursor.execute(sql, (expense_id,))
            self.connection.commit()

            print("\nExpense deleted successfully!")

        except Exception as e:
            print("\nError:", e)

    # ==========================================
    # GET TOTAL EXPENSE
    # ==========================================

    def get_total_expense(self):

        sql = """
        SELECT SUM(amount)
        FROM Expenses
        WHERE user_id = %s
        """

        try:

            self.cursor.execute(sql, (self.user["user_id"],))

            total = self.cursor.fetchone()[0]

            if total is None:

                total = 0

            return float(total)

        except Exception as e:

            print("\nError:", e)

            return 0
    # ==========================================
    # TOTAL EXPENSE
    # ==========================================

    def total_expense(self):

        total = self.get_total_expense()

        print("\n" + "=" * 40)
        print(f"Total Expense : ₹{total:.2f}")
        print("=" * 40)
    # ==========================================
    # SEARCH BY CATEGORY
    # ==========================================

    def search_by_category(self):

        category = self.choose_category()

        sql = """
        SELECT
            expense_id,
            expense_name,
            category,
            amount,
            expense_date,
            description
        FROM Expenses
        WHERE user_id = %s
        AND category = %s
        ORDER BY expense_date DESC
        """

        try:

            self.cursor.execute(
                sql,
                (self.user["user_id"], category)
            )

            expenses = self.cursor.fetchall()

            if not expenses:
                print("\nNo expenses found in this category.")
                return

            print(f"\nCategory : {category}\n")

            print(
                f"{'ID':<5}"
                f"{'Expense Type':<20}"
                f"{'Amount':<12}"
                f"{'Date':<22}"
                f"Description"
            )

            print("-" * 90)

            for expense in expenses:

                date = expense[4].strftime("%d-%b-%Y %I:%M %p")

                print(
                    f"{expense[0]:<5}"
                    f"{expense[1]:<20}"
                    f"₹{expense[3]:<10.2f}"
                    f"{date:<22}"
                    f"{expense[5]}"
                )

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
