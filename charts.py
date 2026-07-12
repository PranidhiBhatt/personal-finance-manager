from database import connect_db

class ChartsManager:

    def __init__(self, user):

        self.user = user

        self.connection = connect_db()

        if self.connection is None:
            raise Exception("Database connection failed.")

        self.cursor = self.connection.cursor()

    # ==========================================
    # EXPENSE By Category
    # ==========================================

    def expense_by_category(self, month):

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

            if not records:

                return []
            
            return records
        
        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # INCOME VS EXPENSE CHART
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
            
            return (
                total_income,
                total_expense
            )
            
        except Exception as e:

            print("\nError:", e)
            return None
        
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

                return []
            
            return records
        
        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # BUDGET VS EXPENSE CHART
    # ==========================================

    def budget_vs_expense(self, month):

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
                return []

            return records

        except Exception as e:

            print("\nError:", e)
            return None

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

                return []

            records = []

            for index in range(len(months)):

                records.append(
                    (
                        months[index],
                        savings[index]
                    )
                )

            return records

        except Exception as e:

            print("\nError:", e)
            return None

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
                return []

            return records

        except Exception as e:

            print("\nError:", e)
            return None

    # ==========================================
    # CLOSE CONNECTION
    #==========================================

    def close_connection(self):

        if self.connection.is_connected():

            self.cursor.close()
            self.connection.close()

            print("\nDatabase connection closed.")
            return None
