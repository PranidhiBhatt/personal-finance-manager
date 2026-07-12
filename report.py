from database import connect_db


class ReportManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()

    # ==========================================
    # MONTHLY EXPENSE REPORT
    # ==========================================

    def monthly_expense_report(self, month):

        sql = """
        SELECT

            category,

            SUM(amount) AS total_expense

        FROM Expenses

        WHERE

            user_id = %s
            AND DATE_FORMAT(expense_date, '%Y-%m') = %s

        GROUP BY

            category

        ORDER BY

            category;
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

                return []

            return records

        except Exception as e:

            print("\nError:", e)

            return None

    # ==========================================
    # MONTHLY INCOME REPORT
    # ==========================================

    def monthly_income_report(self, month):

        sql = """
        SELECT

            source,

            SUM(amount) AS total_income

        FROM Income

        WHERE

            user_id = %s
            AND DATE_FORMAT(income_date, '%Y-%m') = %s

        GROUP BY

            source

        ORDER BY

            source;
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

                return []

            return records

        except Exception as e:

            print("\nError:", e)

            return None

    # ==========================================
    # BUDGET ANALYSIS
    # ==========================================

    def budget_analysis(self, month):

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

                return []

            report = []

            for row in records:

                category = row[0]
                budget = float(row[1])
                spent = float(row[2])
                remaining = float(row[3])

                if remaining >= 0:

                    status = "Within Budget"

                else:

                    status = "Exceeded"

                report.append(
                    (
                        category,
                        budget,
                        spent,
                        remaining,
                        status
                    )
                )

            return report

        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # BUDGET SUMMARY
    # ==========================================

    def budget_summary(self, month):

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

            status = "Within Budget"

            if remaining < 0:

                status = "Budget Exceeded"

            return (
                total_budget,
                total_expense,
                remaining,
                utilization,
                status
            )

        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # OVERSPENDING ALERTS
    # ==========================================

    def overspending_alerts(self, month):

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
                return []

            return records

        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # FINANCIAL DASHBOARD
    # ==========================================

    def financial_dashboard(self, month):

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
                
            status = "Within Budget"

            if remaining_budget < 0:

                status = "Budget Exceeded"

            return (
                total_income,
                total_expense,
                total_budget,
                savings,
                remaining_budget,
                utilization,
                status
            )

        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # INCOME VS EXPENSE
    # ==========================================

    def income_vs_expense(self, month):

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
            
            if difference >= 0:

                result = "Profit"

            else:

                result = "Loss"

            return (
                total_income,
                total_expense,
                difference,
                result
            )

        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # SAVINGS REPORT
    # ==========================================

    def savings_report(self, month):

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

            return (
                total_income,
                total_expense,
                savings,
                savings_rate
            )

        except Exception as e:

            print("\nError:", e)
            return None

# ==========================================
# CLOSE CONNECTION
# ==========================================

    def close_connection(self):

        if self.connection.is_connected():

            self.cursor.close()

            self.connection.close()

            print("\nDatabase connection closed.")
