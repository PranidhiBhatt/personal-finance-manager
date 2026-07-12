import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

class ChartsPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        charts_manager
    ):

        super().__init__(parent)

        self.charts_manager = charts_manager

    # ==========================================
    # Title
    # ==========================================

        title = ctk.CTkLabel(
            self,
            text="Charts",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=20
        )

    # ==========================================
    # Form
    # ==========================================

        form = ctk.CTkFrame(self)

        form.pack(
            padx=20,
            pady=20,
            fill="x"
        )

    # ==========================================
    # Month Entry
    # ==========================================

        ctk.CTkLabel(
            form,
            text="Month"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.month_entry = ctk.CTkEntry(
            form,
            width=300,
            placeholder_text="YYYY-MM"
        )

        self.month_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

    # ==========================================
    # Chart Type
    # ==========================================

        ctk.CTkLabel(
            form,
            text="Chart Type"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.chart_type = ctk.CTkComboBox(
            form,
            width=300,
            values=[
                "Expense by Category",
                "Monthly Expense Trend",
                "Income vs Expense",
                "Savings Trend",
                "Budget vs Expense"
            ]
        )

        self.chart_type.grid(
            row=1,
            column=1,
            padx=10,
            pady=15
        )

    # ==========================================
    # Buttons
    # ==========================================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=15
        )

        self.generate_button = ctk.CTkButton(
            button_frame,
            text="Generate Chart",
            command=self.generate_chart
        )

        self.generate_button.pack(
            side="left",
            padx=10
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_chart
        )

        self.clear_button.pack(
            side="left",
            padx=10
        )

    # ==========================================
    # Chart Frame
    # ==========================================

        self.chart_frame = ctk.CTkFrame(self)

        self.chart_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.chart_canvas = None

    def generate_chart(self):

        month = self.month_entry.get().strip()

        if len(month) != 7 or month[4] != "-":

            CTkMessagebox(
                title="Error",
                message="Please enter the month in YYYY-MM format.",
                icon="cancel"
            )

            return
            
        chart = self.chart_type.get()

        if self.chart_canvas is not None:

            self.chart_canvas.get_tk_widget().destroy()

            self.chart_canvas = None

        if chart == "Expense by Category":

            data = self.charts_manager.expense_by_category(month)

        elif chart == "Monthly Expense Trend":

            data = self.charts_manager.monthly_expense_trend()

        elif chart == "Income vs Expense":

            data = self.charts_manager.income_vs_expense(month)

        elif chart == "Savings Trend":

            data = self.charts_manager.savings_trend()

        elif chart == "Budget vs Expense":

            data = self.charts_manager.budget_vs_expense(month)

        else:

            data = None

        if data is None:

            CTkMessagebox(
                title="Error",
                message="Unable to generate chart.",
                icon="cancel"
            )

            return

        if data == []:

            CTkMessagebox(
                title="No Data",
                message="No records found.",
                icon="info"
            )

            return

        if chart == "Expense by Category":

            self.show_expense_by_category(
                data,
                month
            )

        elif chart == "Monthly Expense Trend":

            self.show_monthly_expense_trend(data)

        elif chart == "Income vs Expense":

            self.show_income_vs_expense(
                data,
                month
            )

        elif chart == "Savings Trend":

            self.show_savings_trend(data)

        elif chart == "Budget vs Expense":

            self.show_budget_vs_expense(
                data,
                month
            )

    # ==========================================
    # EXPENSE BY CATEGORY
    # ==========================================

    def show_expense_by_category(
        self,
        data,
        month
    ):

        labels = []
        amounts = []

        for row in data:

            labels.append(row[0])
            amounts.append(float(row[1]))

        figure = plt.Figure(
            figsize=(6, 5)
        )

        axis = figure.add_subplot(111)

        axis.pie(
            amounts,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        axis.set_title(
            f"Expense by Category ({month})"
        )

        self.chart_canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        self.chart_canvas.draw()

        self.chart_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ==========================================
    # MONTHLY EXPENSE TREND
    # ==========================================

    def show_monthly_expense_trend(
        self,
        data
    ):

        months = []
        expenses = []

        for row in data:

            months.append(row[0])
            expenses.append(float(row[1]))

        figure = plt.Figure(
            figsize=(7, 5)
        )

        axis = figure.add_subplot(111)

        axis.plot(
            months,
            expenses,
            marker="o",
            linewidth=2
        )

        axis.set_title("Monthly Expense Trend")

        axis.set_xlabel("Month")

        axis.set_ylabel("Expense (₹)")

        axis.grid(True)

        self.chart_canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        self.chart_canvas.draw()

        self.chart_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ==========================================
    # INCOME VS EXPENSE
    # ==========================================

    def show_income_vs_expense(
        self,
        data,
        month
    ):

        income = float(data[0])

        expense = float(data[1])

        labels = [
            "Income",
            "Expense"
        ]

        amounts = [
            income,
            expense
        ]

        figure = plt.Figure(
            figsize=(6, 5)
        )

        axis = figure.add_subplot(111)

        bars = axis.bar(
            labels,
            amounts
        )

        axis.set_title(
            f"Income vs Expense ({month})"
        )

        axis.set_ylabel("Amount (₹)")

        for bar in bars:

            height = bar.get_height()

            axis.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"₹{height:.2f}",
                ha="center",
                va="bottom"
            )

        self.chart_canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        self.chart_canvas.draw()

        self.chart_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ==========================================
    # SAVINGS TREND
    # ==========================================

    def show_savings_trend(
        self,
        data
    ):

        months = []
        savings = []

        for row in data:

            months.append(row[0])
            savings.append(float(row[1]))

        figure = plt.Figure(
            figsize=(7, 5)
        )

        axis = figure.add_subplot(111)

        axis.plot(
            months,
            savings,
            marker="o",
            linewidth=2
        )

        axis.set_title("Savings Trend")

        axis.set_xlabel("Month")

        axis.set_ylabel("Savings (₹)")

        axis.grid(True)

        self.chart_canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        self.chart_canvas.draw()

        self.chart_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ==========================================
    # BUDGET VS EXPENSE
    # ==========================================

    def show_budget_vs_expense(
        self,
        data,
        month
    ):

        categories = []
        budgets = []
        expenses = []

        for row in data:

            categories.append(row[0])
            budgets.append(float(row[1]))
            expenses.append(float(row[2]))

        x = np.arange(len(categories))

        width = 0.35

        figure = plt.Figure(
            figsize=(8, 5)
        )

        axis = figure.add_subplot(111)

        axis.bar(
            x - width / 2,
            budgets,
            width,
            label="Budget"
        )

        axis.bar(
            x + width / 2,
            expenses,
            width,
            label="Expense"
        )

        axis.set_xticks(x)

        axis.set_xticklabels(categories)

        axis.set_title(
            f"Budget vs Expense ({month})"
        )

        axis.set_xlabel("Category")

        axis.set_ylabel("Amount (₹)")

        axis.legend()

        self.chart_canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        self.chart_canvas.draw()

        self.chart_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def clear_chart(self):

        self.month_entry.delete(0, "end")

        self.chart_type.set("Expense by Category")

        if self.chart_canvas is not None:

            self.chart_canvas.get_tk_widget().destroy()

            self.chart_canvas = None

