from database import connect_db
from models import Budget

class BudgetManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()

# ==========================================
# MONTH
# ==========================================

    def validate_month(self):

        while True:

            month = input("Month (YYYY-MM): ").strip()

            if month != "":
                return month

            print("Month cannot be empty.")

# ==========================================
# CATEGORY
# ==========================================

    def validate_category(self):

        while True:

            category = input("Budget Category: ").strip()

            if category != "":
                return category

            print("Budget Category cannot be empty.")

# ==========================================
# AMOUNT
# ==========================================

    def validate_amount(self):

        while True:

            try:

                amount = float(input("Budget Amount (₹): "))

                if amount > 0:
                    return amount

                print("Amount must be greater than zero.")

            except ValueError:

                print("Enter a valid amount.")

# ==========================================
# ADD BUDGET DATA
# ==========================================

    def add_budget_data(
        self,
        category,
        budget_amount,
        month,
        user_id
    ):

        budget = Budget(
            None,
            user_id,
            category,
            budget_amount,
            month
        )

        sql = """
        INSERT INTO Budgets
        (user_id, category, budget_amount, month)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            budget.user_id,
            budget.category,
            budget.budget_amount,
            budget.month
        )

        try:

            self.cursor.execute(sql, values)

            self.connection.commit()

            return True

        except Exception as e:

            print("\nError:", e)

            return False

# ==========================================
# ADD BUDGET
# ==========================================

# ==========================================
# ADD BUDGET
# ==========================================

    def add_budget(self):

        print("\n" + "=" * 50)
        print("ADD BUDGET")
        print("=" * 50)

        user_id = self.user["user_id"]

        category = self.validate_category()
        amount = self.validate_amount()
        month = self.validate_month()

        success = self.add_budget_data(
            category,
            amount,
            month,
            user_id
        )

        if success:

            print("\nBudget added successfully!")
# ==========================================
# SHOW BUDGETS
# ==========================================

    def show_budget(self):

        sql = """
        SELECT
        budget_id,
        category,
        budget_amount,
        month
        FROM Budgets
        WHERE user_id=%s
        ORDER BY month DESC, category
        """

        try:

            self.cursor.execute(sql, (self.user["user_id"],))

            budgets = self.cursor.fetchall()

            if not budgets:

                print("\nNo budget records found.\n")
                return

            print("\n" + "=" * 70)
            print(f"Budget Records for {self.user['name']}")
            print("=" * 70)

            print(
                f"{'ID':<5}"
                f"{'Category':<20}"
                f"{'Budget':<15}"
                f"{'Month'}"
            )

            print("-"*70)

            for budget in budgets:

                print(
                    f"{budget[0]:<5}"
                    f"{budget[1]:<20}"
                    f"₹{budget[2]:<13.2f}"
                    f"{budget[3]}"
                )
            print()

        except Exception as e:

            print("\nError:", e)

# ==========================================
# UPDATE BUDGET
# ==========================================

    def update_budget(self):

        self.show_budget()

        try:

            budget_id = int(input("\nEnter Budget ID to update: "))

        except ValueError:

            print("Invalid Budget ID.")
            return

        sql = """
        SELECT budget_id
        FROM Budgets
        WHERE budget_id = %s
        AND user_id = %s
        """

        self.cursor.execute(sql, (budget_id, self.user["user_id"]))

        if self.cursor.fetchone() is None:

            print("\nBudget record not found.")
            return

        print("\nLeave a field blank to keep the current value.\n")

        category = input("New Category: ").strip()
        amount = input("New Budget Amount: ").strip()
        month = input("New Month (YYYY-MM): ").strip()

        updates = []
        values = []

        if category:

            updates.append("category = %s")
            values.append(category)

        if amount:

            try:

                amount = float(amount)

                if amount <= 0:

                    print("Amount must be greater than zero.")
                    return

                updates.append("budget_amount = %s")
                values.append(amount)

            except ValueError:

                print("Invalid amount.")
                return

        if month:

            updates.append("month = %s")
            values.append(month)

        if not updates:

            print("\nNothing to update.")
            return

        sql = f"""
        UPDATE Budgets
        SET {', '.join(updates)}
        WHERE budget_id = %s
        """

        values.append(budget_id)

        try:

            self.cursor.execute(sql, tuple(values))

            self.connection.commit()

            print("\nBudget updated successfully!")

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # GET TOTAL BUDGET
    # ==========================================

    def get_total_budget(self):

        sql = """
        SELECT SUM(budget_amount)
        FROM Budgets
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
# TOTAL BUDGET
# ==========================================

    def total_budget(self):

        total = self.get_total_budget()

        print("\n" + "=" * 40)
        print(f"Total Budget : ₹{total:.2f}")
        print("=" * 40)

# ==========================================
# DELETE BUDGET
# ==========================================


    def delete_budget(self):

        self.show_budget()

        try:

            budget_id = int(input("\nEnter Budget ID to delete: "))

        except ValueError:

            print("Invalid Budget ID.")
            return

        sql = """
        SELECT budget_id
        FROM Budgets
        WHERE budget_id = %s
        AND user_id = %s
        """

        self.cursor.execute(sql, (budget_id, self.user["user_id"]))

        if self.cursor.fetchone() is None:

            print("\nBudget record not found.")
            return

        confirm = input("Are you sure? (y/n): ").lower()

        if confirm != "y":

            print("\nDeletion cancelled.")
            return

        sql = """
        DELETE FROM Budgets
        WHERE budget_id = %s
        """

        try:

            self.cursor.execute(sql, (budget_id,))

            self.connection.commit()

            print("\nBudget deleted successfully!")

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
