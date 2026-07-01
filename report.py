from database import connect_db


class ReportManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()
    # ==========================================
    # BUDGET ANALYSIS
    # ==========================================

    def budget_analysis(self):

        month = input("\nEnter Month (YYYY-MM): ").strip()

        sql = """
        SELECT

            b.category,

            b.budget_amount,

            COALESCE(SUM(e.amount),0) AS spent,

            (b.budget_amount - COALESCE(SUM(e.amount),0)) AS remaining

        FROM Budgets b

        LEFT JOIN Expenses e

            ON b.user_id = e.user_id
            AND b.category = e.category
            AND DATE_FORMAT(e.expense_date, '%Y-%m') = b.month

        WHERE

            b.user_id = %s
            AND b.month = %s

        GROUP BY

            b.category,
            b.budget_amount,
            b.month

        ORDER BY b.category;
        """

        try:

            self.cursor.execute(
                sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            records = self.cursor.fetchall()

            if not records:

                print("\nNo budget found for this month.")
                return

            print("\n" + "=" * 95)
            print(f"          BUDGET ANALYSIS ({month})")
            print("=" * 95)

            print(
                f"{'Category':<20}"
                f"{'Budget':<15}"
                f"{'Spent':<15}"
                f"{'Remaining':<18}"
                f"{'Status'}"
            )

            print("-" * 95)

            total_budget = 0
            total_spent = 0

            for row in records:

                category = row[0]
                budget = float(row[1])
                spent = float(row[2])
                remaining = float(row[3])

                total_budget += budget
                total_spent += spent

                if remaining >= 0:
                    status = "Within Budget"
                else:
                    status = "Exceeded"

                print(
                    f"{category:<20}"
                    f"₹{budget:<14.2f}"
                    f"₹{spent:<14.2f}"
                    f"₹{remaining:<17.2f}"
                    f"{status}"
                )

            print("-" * 95)

            print(f"Total Budget : ₹{total_budget:.2f}")
            print(f"Total Spent  : ₹{total_spent:.2f}")
            print(f"Remaining    : ₹{(total_budget-total_spent):.2f}")

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # BUDGET SUMMARY
    # ==========================================

    def budget_summary(self):

        month = input("\nEnter Month (YYYY-MM): ").strip()

        budget_sql = """
        SELECT COALESCE(SUM(budget_amount), 0)
        FROM Budgets
        WHERE user_id = %s
        AND month = %s
        """

        expense_sql = """
        SELECT COALESCE(SUM(amount), 0)
        FROM Expenses
        WHERE user_id = %s
        AND DATE_FORMAT(expense_date, '%Y-%m') = %s
        """

        try:

            # Total Budget
            self.cursor.execute(
                budget_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_budget = float(self.cursor.fetchone()[0])

            # Total Expenses
            self.cursor.execute(
                expense_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_expense = float(self.cursor.fetchone()[0])

            remaining = total_budget - total_expense

            if total_budget > 0:

                utilization = (total_expense / total_budget) * 100

            else:

                utilization = 0

            print("\n" + "=" * 50)
            print("           BUDGET SUMMARY")
            print("=" * 50)

            print(f"Month               : {month}")
            print(f"Total Budget        : ₹{total_budget:.2f}")
            print(f"Total Expenses      : ₹{total_expense:.2f}")
            print(f"Remaining Budget    : ₹{remaining:.2f}")
            print(f"Budget Utilization  : {utilization:.2f}%")

            if remaining >= 0:

                print("\nStatus : Within Budget ✅")

            else:

                print("\nStatus : Budget Exceeded ❌")

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # OVERSPENDING ALERTS
    # ==========================================

    def overspending_alerts(self):

        month = input("\nEnter Month (YYYY-MM): ").strip()

        sql = """
        SELECT

            b.category,

            b.budget_amount,

            COALESCE(SUM(e.amount), 0) AS spent,

            COALESCE(SUM(e.amount), 0) - b.budget_amount AS exceeded_by

        FROM Budgets b

        LEFT JOIN Expenses e

            ON b.user_id = e.user_id
            AND b.category = e.category
            AND DATE_FORMAT(e.expense_date, '%Y-%m') = b.month

        WHERE

            b.user_id = %s
            AND b.month = %s

        GROUP BY

            b.category,
            b.budget_amount,
            b.month

        HAVING spent > b.budget_amount

        ORDER BY exceeded_by DESC;
        """

        try:

            self.cursor.execute(
                sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            records = self.cursor.fetchall()

            if not records:

                print("\nNo overspending found. Great job! 🎉")
                return

            print("\n" + "=" * 60)
            print("           OVERSPENDING ALERTS")
            print("=" * 60)

            for row in records:

                print(f"\nCategory     : {row[0]}")
                print(f"Budget       : ₹{row[1]:.2f}")
                print(f"Spent        : ₹{row[2]:.2f}")
                print(f"Exceeded By  : ₹{row[3]:.2f}")

                print("-" * 60)

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # FINANCIAL DASHBOARD
    # ==========================================

    def financial_dashboard(self):

        month = input("\nEnter Month (YYYY-MM): ").strip()

        try:

            # Total Income
            income_sql = """
            SELECT COALESCE(SUM(amount),0)
            FROM Income
            WHERE user_id=%s
            AND DATE_FORMAT(income_date,'%Y-%m')=%s
            """

            self.cursor.execute(
                income_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_income = float(self.cursor.fetchone()[0])

            # Total Expenses
            expense_sql = """
            SELECT COALESCE(SUM(amount),0)
            FROM Expenses
            WHERE user_id=%s
            AND DATE_FORMAT(expense_date,'%Y-%m')=%s
            """

            self.cursor.execute(
                expense_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_expense = float(self.cursor.fetchone()[0])

            # Total Budget
            budget_sql = """
            SELECT COALESCE(SUM(budget_amount),0)
            FROM Budgets
            WHERE user_id=%s
            AND month=%s
            """

            self.cursor.execute(
                budget_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_budget = float(self.cursor.fetchone()[0])

            savings = total_income - total_expense

            remaining_budget = total_budget - total_expense

            if total_budget > 0:

                utilization = (total_expense / total_budget) * 100

            else:

                utilization = 0

            print("\n" + "=" * 60)
            print("              FINANCIAL DASHBOARD")
            print("=" * 60)

            print(f"Month               : {month}")
            print(f"Total Income        : ₹{total_income:.2f}")
            print(f"Total Expenses      : ₹{total_expense:.2f}")
            print(f"Total Budget        : ₹{total_budget:.2f}")
            print("-" * 60)
            print(f"Savings             : ₹{savings:.2f}")
            print(f"Budget Remaining    : ₹{remaining_budget:.2f}")
            print(f"Budget Utilization  : {utilization:.2f}%")

            if remaining_budget >= 0:

                print("\nStatus : Within Budget ✅")

            else:

                print("\nStatus : Budget Exceeded ❌")

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # INCOME VS EXPENSE
    # ==========================================

    def income_vs_expense(self):

        month = input("\nEnter Month (YYYY-MM): ").strip()

        income_sql = """
        SELECT COALESCE(SUM(amount),0)
        FROM Income
        WHERE user_id=%s
        AND DATE_FORMAT(income_date,'%Y-%m')=%s
        """

        expense_sql = """
        SELECT COALESCE(SUM(amount),0)
        FROM Expenses
        WHERE user_id=%s
        AND DATE_FORMAT(expense_date,'%Y-%m')=%s
        """

        try:

            self.cursor.execute(
                income_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_income = float(self.cursor.fetchone()[0])

            self.cursor.execute(
                expense_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_expense = float(self.cursor.fetchone()[0])

            difference = total_income - total_expense

            print("\n" + "=" * 50)
            print("         INCOME VS EXPENSE")
            print("=" * 50)

            print(f"Month           : {month}")
            print(f"Total Income    : ₹{total_income:.2f}")
            print(f"Total Expense   : ₹{total_expense:.2f}")
            print(f"Difference      : ₹{difference:.2f}")

            if difference >= 0:
                print("\nResult : Profit 📈")
            else:
                print("\nResult : Loss 📉")

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # SAVINGS REPORT
    # ==========================================

    def savings_report(self):

        month = input("\nEnter Month (YYYY-MM): ").strip()

        income_sql = """
        SELECT COALESCE(SUM(amount),0)
        FROM Income
        WHERE user_id=%s
        AND DATE_FORMAT(income_date,'%Y-%m')=%s
        """

        expense_sql = """
        SELECT COALESCE(SUM(amount),0)
        FROM Expenses
        WHERE user_id=%s
        AND DATE_FORMAT(expense_date,'%Y-%m')=%s
        """

        try:

            self.cursor.execute(
                income_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_income = float(self.cursor.fetchone()[0])

            self.cursor.execute(
                expense_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_expense = float(self.cursor.fetchone()[0])

            savings = total_income - total_expense

            if total_income > 0:
                savings_rate = (savings / total_income) * 100
            else:
                savings_rate = 0

            print("\n" + "=" * 50)
            print("           SAVINGS REPORT")
            print("=" * 50)

            print(f"Month          : {month}")
            print(f"Income         : ₹{total_income:.2f}")
            print(f"Expenses       : ₹{total_expense:.2f}")
            print(f"Savings        : ₹{savings:.2f}")
            print(f"Savings Rate   : {savings_rate:.2f}%")

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
