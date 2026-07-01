from database import connect_db
import matplotlib.pyplot as plt


class ChartManager:

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

            month = input("Enter Month (YYYY-MM): ").strip()

            if len(month) == 7 and month[4] == "-":
                return month

            print("Invalid format. Use YYYY-MM.")

    # ==========================================
    # EXPENSE DISTRIBUTION
    # ==========================================

    def expense_distribution(self):

        month = self.validate_month()

        sql = """
        SELECT
            category,
            SUM(amount)
        FROM Expenses
        WHERE user_id=%s
        AND DATE_FORMAT(expense_date,'%Y-%m')=%s
        GROUP BY category
        ORDER BY SUM(amount) DESC
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
            print(records)

            if not records:

                print("\nNo expenses found.")
                return

            categories = []
            amounts = []

            for row in records:

                categories.append(row[0])
                amounts.append(float(row[1]))

            plt.figure(figsize=(8,8))

            plt.pie(
                amounts,
                labels=categories,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title(f"Expense Distribution ({month})")

            plt.axis("equal")

            plt.show()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # INCOME VS EXPENSE CHART
    # ==========================================

    def income_vs_expense_chart(self):

        month = self.validate_month()

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

            # Total Income
            self.cursor.execute(
                income_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_income = float(self.cursor.fetchone()[0])

            # Total Expense
            self.cursor.execute(
                expense_sql,
                (
                    self.user["user_id"],
                    month
                )
            )

            total_expense = float(self.cursor.fetchone()[0])

            labels = ["Income", "Expense"]
            amounts = [total_income, total_expense]

            plt.figure(figsize=(6, 5))

            plt.bar(labels, amounts)

            plt.title(f"Income vs Expense ({month})")
            plt.xlabel("Category")
            plt.ylabel("Amount (₹)")

            for i, value in enumerate(amounts):
                plt.text(i, value, f"₹{value:.2f}", ha="center", va="bottom")

            plt.tight_layout()
            plt.show()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # MONTHLY EXPENSE TREND
    # ==========================================

    def monthly_expense_trend(self):

        sql = """
        SELECT

            DATE_FORMAT(expense_date,'%Y-%m') AS month,

            SUM(amount)

        FROM Expenses

        WHERE user_id=%s

        GROUP BY DATE_FORMAT(expense_date,'%Y-%m')

        ORDER BY month;
        """

        try:

            self.cursor.execute(
                sql,
                (
                    self.user["user_id"],
                )
            )

            records = self.cursor.fetchall()

            if not records:

                print("\nNo expense records found.")
                return

            months = []
            expenses = []

            for row in records:

                months.append(row[0])
                expenses.append(float(row[1]))

            plt.figure(figsize=(8,5))

            plt.plot(
                months,
                expenses,
                marker="o",
                linewidth=2
            )

            plt.title("Monthly Expense Trend")

            plt.xlabel("Month")

            plt.ylabel("Expense (₹)")

            plt.grid(True)

            plt.tight_layout()

            plt.show()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # BUDGET VS EXPENSE CHART
    # ==========================================

    def budget_vs_expense_chart(self):

        month = self.validate_month()

        sql = """
        SELECT
            b.category,
            b.budget_amount,
            COALESCE(e.total_expense, 0) AS expense
        FROM Budgets b
        LEFT JOIN
        (
            SELECT
                category,
                user_id,
                DATE_FORMAT(expense_date,'%Y-%m') AS month,
                SUM(amount) AS total_expense
            FROM Expenses
            GROUP BY
                user_id,
                category,
                DATE_FORMAT(expense_date,'%Y-%m')
        ) e
        ON b.user_id = e.user_id
        AND b.category = e.category
        AND b.month = e.month
        WHERE b.user_id = %s
        AND b.month = %s
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

                print("\nNo budget records found.")
                return

            categories = []
            budgets = []
            expenses = []

            for row in records:

                categories.append(row[0])
                budgets.append(float(row[1]))
                expenses.append(float(row[2]))

            import numpy as np

            x = np.arange(len(categories))
            width = 0.35

            plt.figure(figsize=(10,6))

            plt.bar(
                x - width/2,
                budgets,
                width,
                label="Budget"
            )

            plt.bar(
                x + width/2,
                expenses,
                width,
                label="Expense"
            )

            plt.xticks(x, categories)

            plt.title(f"Budget vs Expense ({month})")

            plt.xlabel("Category")
            plt.ylabel("Amount (₹)")

            plt.legend()

            plt.tight_layout()

            plt.show()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # SAVINGS TREND
    # ==========================================

    def savings_trend(self):

        income_sql = """
        SELECT
            DATE_FORMAT(income_date,'%Y-%m') AS month,
            SUM(amount)
        FROM Income
        WHERE user_id=%s
        GROUP BY DATE_FORMAT(income_date,'%Y-%m')
        """

        expense_sql = """
        SELECT
            DATE_FORMAT(expense_date,'%Y-%m') AS month,
            SUM(amount)
        FROM Expenses
        WHERE user_id=%s
        GROUP BY DATE_FORMAT(expense_date,'%Y-%m')
        """

        try:

            self.cursor.execute(income_sql, (self.user["user_id"],))
            income_records = self.cursor.fetchall()

            self.cursor.execute(expense_sql, (self.user["user_id"],))
            expense_records = self.cursor.fetchall()

            income_dict = {row[0]: float(row[1]) for row in income_records}
            expense_dict = {row[0]: float(row[1]) for row in expense_records}

            months = sorted(set(income_dict.keys()) | set(expense_dict.keys()))

            savings = []

            for month in months:

                income = income_dict.get(month, 0)
                expense = expense_dict.get(month, 0)

                savings.append(income - expense)

            if not months:

                print("\nNo records found.")
                return

            plt.figure(figsize=(8,5))

            plt.plot(
                months,
                savings,
                marker="o",
                linewidth=2
            )

            plt.title("Monthly Savings Trend")
            plt.xlabel("Month")
            plt.ylabel("Savings (₹)")

            plt.grid(True)

            plt.tight_layout()

            plt.show()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # TOP SPENDING CATEGORIES
    # ==========================================

    def top_spending_categories(self):

        sql = """
        SELECT
            category,
            SUM(amount) AS total
        FROM Expenses
        WHERE user_id = %s
        GROUP BY category
        ORDER BY total DESC;
        """

        try:

            self.cursor.execute(
                sql,
                (
                    self.user["user_id"],
                )
            )

            records = self.cursor.fetchall()

            if not records:

                print("\nNo expense records found.")
                return

            categories = []
            totals = []

            for row in records:

                categories.append(row[0])
                totals.append(float(row[1]))

            plt.figure(figsize=(8,5))

            plt.barh(categories, totals)

            plt.title("Top Spending Categories")

            plt.xlabel("Amount (₹)")
            plt.ylabel("Category")

            plt.tight_layout()

            plt.show()

        except Exception as e:

            print("\nError:", e)

    # ==========================================
    # CLOSE CONNECTION
    #==========================================

    def close_connection(self):

        if self.connection.is_connected():

            self.cursor.close()
            self.connection.close()

            print("\nDatabase connection closed.")
