from auth import AuthManager
from expense import ExpenseManager
from income import IncomeManager


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

        while True:

            print("\n" + "=" * 50)
            print(f"Welcome, {user['name']}")
            print("=" * 50)

            print("1. Expense Management")
            print("2. Income Management")
            print("3. Budget Management")
            print("4. Reports")
            print("5. Logout")

            choice = input("\nEnter Choice: ")

            if choice == "1":

                self.expense_menu(expense)

            elif choice == "2":

                self.income_menu(income)

            elif choice == "3":

                print("\nBudget Module Coming Soon!")

            elif choice == "4":

                print("\nReports Module Coming Soon!")

            elif choice == "5":

                expense.close_connection()
                income.close_connection()

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
                
if __name__ == "__main__":

    app = PersonalFinanceManager()

    app.start()
