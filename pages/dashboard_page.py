import customtkinter as ctk


class DashboardPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        user,
        expense_manager,
        income_manager,
        budget_manager
    ):

        super().__init__(parent)

        self.user = user
        self.expense_manager = expense_manager
        self.income_manager = income_manager
        self.budget_manager = budget_manager

        top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top.pack(pady=20)

        bottom = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom.pack(pady=20)

        self.income_card, self.income_value = self.create_card(
            top,
            "Total Income"
        )

        self.income_card.pack(
            side="left",
            padx=15
        )

        self.expense_card, self.expense_value = self.create_card(
            top,
            "Total Expense"
        )

        self.expense_card.pack(
            side="left",
            padx=15
        )

        self.savings_card, self.savings_value = self.create_card(
            bottom,
            "Savings"
        )

        self.savings_card.pack(
            side="left",
            padx=15
        )

        self.budget_card, self.budget_value = self.create_card(
            bottom,
            "Total Budget"
        )

        self.budget_card.pack(
            side="left",
            padx=15
        )

        self.update_dashboard()

    def create_card(self, parent, title):

        frame = ctk.CTkFrame(
            parent,
            width=250,
            height=120,
            corner_radius=15
        )

        frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 18, "bold")
        )

        title_label.pack(
            pady=(20, 5)
        )

        value = ctk.CTkLabel(
            frame,
            text="₹0",
            font=("Arial", 24)
        )

        value.pack()

        return frame, value

    def update_dashboard(self):

        income = self.income_manager.get_total_income()

        expense = self.expense_manager.get_total_expense()

        budget = self.budget_manager.total_budget()

        savings = income - expense

        self.income_value.configure(
            text=f"₹{income:,.2f}"
        )

        self.expense_value.configure(
            text=f"₹{expense:,.2f}"
        )

        self.savings_value.configure(
            text=f"₹{savings:,.2f}"
        )

        self.budget_value.configure(
            text=f"₹{budget:,.2f}"
        )

