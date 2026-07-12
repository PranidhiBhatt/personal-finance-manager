from auth import AuthManager
from login import LoginWindow

from expense import ExpenseManager
from income import IncomeManager
from budget import BudgetManager
from report import ReportManager
from charts import ChartsManager


class PersonalFinanceManager:

    def __init__(self):

        self.auth = AuthManager()

    # ==========================================
    # LOGIN MENU
    # ==========================================

    def start(self):

        while True:

            print("\n" + "=" * 50)
            print("      PERSONAL FINANCE MANAGER")
            print("=" * 50)

            print("1. Login")
            print("2. Exit")

            choice = input("\nEnter Choice: ")

            if choice == "1":

                user = self.auth.login()

                if user:
                    self.main_menu(user)

            elif choice == "2":

                self.auth.close_connection()

                print("\nThank you for using Personal Finance Manager!")

                break

            else:

                print("\nInvalid Choice.")
    # ==========================================
    # MAIN MENU
    # ==========================================

    def main_menu(self, user):

        expense = ExpenseManager(user)
        income = IncomeManager(user)
        budget = BudgetManager(user)
        report = ReportManager(user)
        charts = ChartManager(user)

        while True:

            print("\n" + "=" * 50)
            print(f"Welcome, {user['name']}")
            print("=" * 50)

            print("1. Expense Management")
            print("2. Income Management")
            print("3. Budget Management")
            print("4. Reports")
            print("5. Charts")
            print("6. Logout")

            choice = input("\nEnter Choice: ")

            if choice == "1":

                self.expense_menu(expense)

            elif choice == "2":

                self.income_menu(income)

            elif choice == "3":

                self.budget_menu(budget)

            elif choice == "4":

                self.report_menu(report)

            elif choice == "5":

                self.chart_menu(charts)

            elif choice == "6":

                expense.close_connection()
                income.close_connection()
                budget.close_connection()
                report.close_connection()
                charts.close_connection()

                print("\nLogged Out Successfully.")

                break

            else:

                print("\nInvalid Choice.")
    # ==========================================
    # EXPENSE MENU
    # ==========================================

    def expense_menu(self, expense):

        while True:

            print("\n" + "=" * 50)
            print("        EXPENSE MANAGEMENT")
            print("=" * 50)

            print("1. Add Expense")
            print("2. Show Expenses")
            print("3. Update Expense")
            print("4. Delete Expense")
            print("5. Search by Category")
            print("6. Total Expense")
            print("7. Back")

            choice = input("\nEnter Choice: ")
            
            if choice == "1":
                
                expense.add_expense()

            elif choice == "2":

                expense.show_expenses()

            elif choice == "3":

                expense.update_expense()

            elif choice == "4":

                expense.delete_expense()

            elif choice == "5":

                expense.search_by_category()

            elif choice == "6":

                expense.total_expense()

            elif choice == "7":

                break

            else:

                print("\nInvalid Choice.")
    # ==========================================
    # INCOME MENU
    # ==========================================

    def income_menu(self, income):
        while True:
            print("\n" + "=" * 50)
            print("         INCOME MANAGEMENT")
            print("=" * 50)

            print("1. Add Income")
            print("2. Show Income")
            print("3. Update Income")
            print("4. Delete Income")
            print("5. Total Income")
            print("6. Back")

            choice = input("\nEnter Choice: ")
        

            if choice == "1":

               income.add_income()

            elif choice == "2":

                income.show_income()
                
            elif choice == "3":
                
                income.update_income()
                
            elif choice == "4":
                
                income.delete_income()
                
            elif choice == "5":
                
                income.total_income()
                
            elif choice == "6":
                
                break
            
            else:
                
                print("\nInvalid Choice.")

    # ==========================================
    # BUDGET MENU
    # ==========================================

    def budget_menu(self, budget):
        while True:
            print("\n" + "=" * 50)
            print("         BUDGET MANAGEMENT")
            print("=" * 50)
            
            print("1. Add Budget")
            print("2. Show Budget")
            print("3. Update Budget")
            print("4. Delete Budget")
            print("5. Total Budget")
            print("6. Back")
            
            choice = input("\nEnter Choice: ")

            if choice == "1":
               budget.add_budget()
            elif choice == "2":
               budget.show_budget()
            elif choice == "3":
               budget.update_budget()
            elif choice == "4":
               budget.delete_budget()
            elif choice == "5":
               budget.total_budget()
            elif choice == "6":
               break
            else:
               print("\nInvalid Choice.")

    # ==========================================
    # REPORT MENU
    # ==========================================

    def report_menu(self, report):

        while True:

            print("\n" + "=" * 50)
            print("            REPORTS")
            print("=" * 50)

            print("1. Financial Dashboard")
            print("2. Budget Analysis")
            print("3. Budget Summary")
            print("4. Overspending Alerts")
            print("5. Income vs Expense")
            print("6. Savings Report")
            print("7. Back")

            choice = input("\nEnter Choice: ")

            if choice == "1":

                report.financial_dashboard()

            elif choice == "2":

                report.budget_analysis()

            elif choice == "3":

                report.budget_summary()

            elif choice == "4":

                report.overspending_alerts()

            elif choice == "5":

                report.income_vs_expense()

            elif choice == "6":

                report.savings_report()

            elif choice == "7":

                break
            
            else:

                print("\nInvalid Choice.")

    # ==========================================
    # CHART MENU
    # ==========================================

    def chart_menu(self, charts):

        while True:

            print("\n" + "=" * 50)
            print("          CHARTS")
            print("=" * 50)

            print("1. Expense Distribution")
            print("2. Income vs Expense")
            print("3. Monthly Expense Trend")
            print("4. Budget vs Expense")
            print("5. Savings Trend")
            print("6. Top Spending Categories")
            print("7. Back")

            choice = input("\nEnter Choice: ")

            if choice == "1":

                charts.expense_distribution()

            elif choice == "2":

                charts.income_vs_expense_chart()

            elif choice == "3":

                charts.monthly_expense_trend()

            elif choice == "4":

                charts.budget_vs_expense_chart()

            elif choice == "5":

                charts.savings_trend()

            elif choice == "6":

                charts.top_spending_categories()

            elif choice == "7":

                break

            else:

                print("\nInvalid Choice.")
                
if __name__ == "__main__":

    app = LoginWindow()

    app.mainloop()
