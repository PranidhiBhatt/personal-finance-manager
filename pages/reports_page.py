import csv
import os

import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class ReportPage(ctk.CTkFrame):

    def __init__(self, parent, report_manager):

        super().__init__(parent)

        self.report_manager = report_manager

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Reports",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=20
        )

        # =====================================
        # FORM
        # =====================================

        form = ctk.CTkFrame(self)

        form.pack(
            padx=20,
            pady=20,
            fill="x"
        )

        # ==========================
        # Month
        # ==========================

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

        # ==========================
        # Report Type
        # ==========================

        ctk.CTkLabel(
            form,
            text="Report Type"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.report_type = ctk.CTkComboBox(
            form,
            width=300,
            values=[
                "Monthly Expense Report",
                "Monthly Income Report",
                "Budget vs Expense Report",
                "Savings Report"
            ]
        )

        self.report_type.grid(
            row=1,
            column=1,
            padx=10,
            pady=15
        )

        # =====================================
        # BUTTONS
        # =====================================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=15
        )

        self.generate_button = ctk.CTkButton(
            button_frame,
            text="Generate Report",
            command=self.generate_report
        )

        self.generate_button.pack(
            side="left",
            padx=10
        )

        self.export_csv_button = ctk.CTkButton(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        )

        self.export_csv_button.pack(
            side="left",
            padx=10
        )

        self.export_pdf_button = ctk.CTkButton(
            button_frame,
            text="Export PDF",
            command=self.export_pdf
        )

        self.export_pdf_button.pack(
            side="left",
            padx=10
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_table
        )

        self.clear_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # TABLE
        # =====================================

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "Data",
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                anchor="center",
                width=180
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.configure_table(
            (
                "Data",
            )
        )

    def generate_report(self):

        month = self.month_entry.get().strip()

        if len(month) != 7 or month[4] != "-":

            CTkMessagebox(
                title="Error",
                message="Please enter the month in YYYY-MM format.",
                icon="cancel"
            )

            return

        report = self.report_type.get()

        for row in self.tree.get_children():

            self.tree.delete(row)
            
        if report == "Monthly Expense Report":

            self.configure_table(
                (
                    "Category",
                    "Expense"
                )
            )

            data = self.report_manager.monthly_expense_report(month)

        elif report == "Monthly Income Report":

            self.configure_table(
                (
                    "Source",
                    "Income"
                )
            )

            data = self.report_manager.monthly_income_report(month)

        elif report == "Budget vs Expense Report":

            self.configure_table(
                (
                    "Category",
                    "Budget",
                    "Spent",
                    "Remaining",
                    "Status"
                )
            )

            data = self.report_manager.budget_analysis(month)

        elif report == "Savings Report":

            self.configure_table(
                (
                    "Income",
                    "Expense",
                    "Savings",
                    "Savings %"
                )
            )

            data = self.report_manager.savings_report(month)

        else:

            data = None

        if data is None:

            CTkMessagebox(
                title="Error",
                message="Unable to generate report.",
                icon="cancel"
            )

            return

        if data == []:

            CTkMessagebox(
                title="No Data",
                message="No records found for this month.",
                icon="info"
            )

            return

        if report == "Savings Report":

            formatted_data = []

            for index, value in enumerate(data):

                if isinstance(value, (int, float)):

                    if index == 3:

                        formatted_data.append(
                            f"{value:.2f}%"
                        )

                    else:

                        formatted_data.append(
                            f"₹{value:,.2f}"
                        )

                else:

                    formatted_data.append(value)

            self.tree.insert(
                "",
                "end",
                values=formatted_data
            )

        else:

            for row in data:

                formatted_row = []

                for value in row:

                    if isinstance(value, (int, float)):

                        formatted_row.append(
                            f"₹{value:,.2f}"
                        )

                    else:

                        formatted_row.append(value)

                self.tree.insert(
                    "",
                    "end",
                    values=formatted_row
                )

    def export_csv(self):

        month = self.month_entry.get().strip()

        if len(month) != 7 or month[4] != "-":

            CTkMessagebox(
                title="Error",
                message="Please enter the month in YYYY-MM format.",
                icon="cancel"
            )

            return

        report = self.report_type.get()

        if report == "Monthly Expense Report":

            data = self.report_manager.monthly_expense_report(month)

            filename = f"monthly_expense_report_{month}.csv"

        elif report == "Monthly Income Report":

            data = self.report_manager.monthly_income_report(month)

            filename = f"monthly_income_report_{month}.csv"

        elif report == "Budget vs Expense Report":

            data = self.report_manager.budget_analysis(month)

            filename = f"budget_vs_expense_report_{month}.csv"

        elif report == "Savings Report":

            data = self.report_manager.savings_report(month)

            filename = f"savings_report_{month}.csv"

        else:

            return

        if data is None:

            CTkMessagebox(
                title="Error",
                message="Unable to export report.",
                icon="cancel"
            )

            return

        if data == []:

            CTkMessagebox(
                title="No Data",
                message="No records found to export.",
                icon="info"
            )

            return

        file_path = os.path.join(
            "reports",
            filename
        )

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if report == "Monthly Expense Report":

                writer.writerow(
                    [
                        "Category",
                        "Expense"
                    ]
                )

            elif report == "Monthly Income Report":

                writer.writerow(
                    [
                        "Source",
                        "Income"
                    ]
                )

            elif report == "Budget vs Expense Report":

                writer.writerow(
                    [
                        "Category",
                        "Budget",
                        "Spent",
                        "Remaining",
                        "Status"
                    ]
                )

            elif report == "Savings Report":

                writer.writerow(
                    [
                        "Income",
                        "Expense",
                        "Savings",
                        "Savings %"
                    ]
                )

            if report == "Savings Report":

                writer.writerow(data)

            else:

                writer.writerows(data)

        CTkMessagebox(
            title="Success",
            message=f"Report exported successfully!\n\nSaved as:\n{filename}",
            icon="check"
        )

    def export_pdf(self):

        pass

    def clear_table(self):

        self.month_entry.delete(0, "end")

        self.report_type.set("Monthly Expense Report")

        for row in self.tree.get_children():

            self.tree.delete(row)

    def configure_table(
        self,
        columns
    ):

        self.tree.configure(
            columns=columns
        )

        self.tree["show"] = "headings"

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                anchor="center",
                width=180
            )
