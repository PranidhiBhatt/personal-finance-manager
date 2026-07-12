import customtkinter as ctk

from expense import ExpenseManager
from income import IncomeManager
from budget import BudgetManager
from report import ReportManager
from charts import ChartsManager
from account import AccountManager

from pages.dashboard_page import DashboardPage
from pages.expense_page import ExpensePage
from pages.income_page import IncomePage
from pages.budgets_page import BudgetPage
from pages.reports_page import ReportPage
from pages.charts_page import ChartsPage
from pages.account_page import AccountPage

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FinanceGUI(ctk.CTk):

    def __init__(self, user):

        super().__init__()
        
        self.user = user

        self.expense_manager = ExpenseManager(user)
        self.income_manager = IncomeManager(user)
        self.budget_manager = BudgetManager(user)
        self.report_manager = ReportManager(user)
        self.charts_manager = ChartsManager(user)
        self.account_manager = AccountManager(user)

        self.title("Personal Finance Manager")

        self.geometry("1200x700")

        self.minsize(1100, 650)

        # ==============================
        # Sidebar
        # ==============================

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="\nFinance\nManager",
            font=("Arial", 24, "bold")
        )

        self.logo.pack(
            pady=30
        )

        buttons = [

            "Dashboard",

            "Expenses",

            "Income",

            "Budget",

            "Reports",

            "Charts",

            "Account",

            "Logout"

        ]

        for name in buttons:

            if name == "Logout":

                command = self.destroy

            elif name in ["Dashboard", "Expenses", "Income", "Budget", "Reports", "Charts", "Account"]:
                command = lambda page=name: self.show_page(page)

            else:

                command = None

            button = ctk.CTkButton(
                self.sidebar,
                text=name,
                width=180,
                height=40,
                command=command
            )

            button.pack(
                pady=8,
                padx=15
            )

        # ==============================
        # Main Area
        # ==============================

        self.main_frame = ctk.CTkFrame(
            self
        )

        self.page_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.page_container.pack(
            fill="both",
            expand=True
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==============================
        # Dashboard
        # ==============================

        self.pages = {}

        self.pages["Dashboard"] = DashboardPage(
            self.page_container,
            self.user,
            self.expense_manager,
            self.income_manager,
            self.budget_manager
        )

        self.pages["Dashboard"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.pages["Expenses"] = ExpensePage(
            self.page_container,
            self.expense_manager,
            self.pages["Dashboard"].update_dashboard
        )

        self.pages["Expenses"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.pages["Income"] = IncomePage(
            self.page_container,
            self.income_manager,
            self.pages["Dashboard"].update_dashboard
        )

        self.pages["Income"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.pages["Budget"] = BudgetPage(
            self.page_container,
            self.budget_manager,
            self.pages["Dashboard"].update_dashboard
        )

        self.pages["Budget"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.pages["Reports"] = ReportPage(
            self.page_container,
            self.report_manager,
        )

        self.pages["Reports"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.pages["Charts"] = ChartsPage(
            self.page_container,
            self.charts_manager,
        )

        self.pages["Charts"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.pages["Account"] = AccountPage(
            self.page_container,
            self.account_manager,
            self.user
        )

        self.pages["Account"].place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )
        
        self.show_page("Dashboard")

    
    def show_page(self, page_name):

        self.pages[page_name].lift()


if __name__ == "__main__":

    user = {
        "user_id": 1,
        "name": "Amit"
    }

    app = FinanceGUI(user)

    app.mainloop()



