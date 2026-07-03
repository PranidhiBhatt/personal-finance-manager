import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from datetime import datetime


class IncomePage(ctk.CTkFrame):

    def __init__(self, parent, income_manager, refresh_dashboard):

        super().__init__(parent)

        self.income_manager = income_manager
        self.refresh_dashboard = refresh_dashboard
        self.selected_income_id = None

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Income Management",
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
            pady=10,
            fill="x"
        )

        # Income Name

        ctk.CTkLabel(
            form,
            text="Income Source"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.name_entry = ctk.CTkEntry(
            form,
            width=250
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Amount

        ctk.CTkLabel(
            form,
            text="Amount"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.amount_entry = ctk.CTkEntry(
            form,
            width=250
        )

        self.amount_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
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

        self.add_button = ctk.CTkButton(
            button_frame,
            text="Add Income",
            command=self.add_income           
        )

        self.add_button.pack(
            side="left",
            padx=10
        )

        self.refresh_button = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.load_income
        )

        self.refresh_button.pack(
            side="left",
            padx=10
        )

        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            fg_color="#C0392B",
            hover_color="#A93226",
            command=self.delete_income
        )

        self.delete_button.pack(
            side="left",
            padx=10
        )

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update Income",
            command=self.update_income
        )

        self.update_button.pack(
            side="left",
            padx=10
        )

        self.update_button.configure(
            state="disabled"
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form
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
            "ID",
            "Source",
            "Amount",
            "Date"
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
                width=140
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

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_income
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.load_income()

    def load_income(self):

        # Clear existing rows
        for row in self.tree.get_children():

            self.tree.delete(row)

        sql = """
        SELECT
            income_id,
            source,
            amount,
            income_date
        FROM Income
        WHERE user_id = %s
        ORDER BY income_date DESC
        """

        try:

            self.income_manager.cursor.execute(
                sql,
                (self.income_manager.user["user_id"],)
            )

            incomes = self.income_manager.cursor.fetchall()

            for income in incomes:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        income[0],
                        income[1],
                        f"₹{income[2]:,.2f}",
                        income[3].strftime("%d-%b-%Y")
                    )
                )

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def add_income(self):

        source = self.name_entry.get().strip()

        amount = self.amount_entry.get().strip()

        if not source:

            CTkMessagebox(
                title="Error",
                message="Income source is required.",
                icon="cancel"
            )
            return

        if not amount:

            CTkMessagebox(
                title="Error",
                message="Amount is required.",
                icon="cancel"
            )
            return

        try:

            amount = float(amount)

        except ValueError:

            CTkMessagebox(
                title="Error",
                message="Please enter a valid amount.",
                icon="cancel"
            )
            return

        sql = """
        INSERT INTO Income
        (user_id, source, amount, income_date)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            self.income_manager.user["user_id"],
            source,
            amount,
            datetime.now()
        )

        try:

            self.income_manager.cursor.execute(sql, values)

            self.income_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Income added successfully!",
                icon="check"
            )

            self.load_income()

            self.refresh_dashboard()

            self.clear_form()

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def clear_form(self):

        self.name_entry.delete(0, "end")

        self.amount_entry.delete(0, "end")

        self.selected_income_id = None

        self.tree.selection_remove(
            self.tree.selection()
        )

        self.update_button.configure(
            state="disabled"
        )

    def delete_income(self):

        selected = self.tree.selection()

        if not selected:

            CTkMessagebox(
                title="Warning",
                message="Please select an income first.",
                icon="warning"
            )
            return

        income_id = self.tree.item(selected[0])["values"][0]

        response = CTkMessagebox(
            title="Confirm Delete",
            message="Are you sure you want to delete this income?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete"
        )

        if response.get() != "Delete":
            return

        sql = """
        DELETE FROM Income
        WHERE income_id = %s
        """

        try:

            self.income_manager.cursor.execute(
                sql,
                (income_id,)
            )

            self.income_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Income deleted successfully!",
                icon="check"
            )

            self.load_income()

            self.refresh_dashboard()

            self.clear_form()

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def select_income(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        self.selected_income_id = values[0]

        self.update_button.configure(state="normal")

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, values[1])

        amount = values[2].replace("₹", "").replace(",", "")

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, amount)
        
    def update_income(self):

        if self.selected_income_id is None:

            CTkMessagebox(
                title="Warning",
                message="Please select an income first.",
                icon="warning"
            )
            return

        source = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not source:

            CTkMessagebox(
                title="Error",
                message="Income source is required.",
                icon="cancel"
            )
            return

        try:

            amount = float(amount)

        except ValueError:

            CTkMessagebox(
                title="Error",
                message="Please enter a valid amount.",
                icon="cancel"
            )
            return

        sql = """
        UPDATE Income
        SET
            source=%s,
            amount=%s
        WHERE income_id=%s
        """

        values = (
            source,
            amount,
            self.selected_income_id
        )

        try:

            self.income_manager.cursor.execute(sql, values)

            self.income_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Income updated successfully!",
                icon="check"
            )

            self.load_income()

            self.refresh_dashboard()

            self.clear_form()

            self.selected_income_id = None

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )
