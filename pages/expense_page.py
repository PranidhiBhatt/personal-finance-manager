import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class ExpensePage(ctk.CTkFrame):

    def __init__(self, parent, expense_manager, refresh_dashboard):

        super().__init__(parent)

        self.expense_manager = expense_manager
        self.refresh_dashboard = refresh_dashboard
        self.selected_expense_id = None

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Expense Management",
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

        # Expense Name

        ctk.CTkLabel(
            form,
            text="Expense Name"
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

        # Category

        ctk.CTkLabel(
            form,
            text="Category"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.category = ctk.CTkComboBox(
            form,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Health",
                "Education",
                "Other"
            ],
            width=250
        )

        self.category.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Amount

        ctk.CTkLabel(
            form,
            text="Amount"
        ).grid(
            row=2,
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
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # Description

        ctk.CTkLabel(
            form,
            text="Description"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.description_entry = ctk.CTkEntry(
            form,
            width=250
        )

        self.description_entry.grid(
            row=3,
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
            text="Add Expense",
            command=self.add_expense           
        )

        self.add_button.pack(
            side="left",
            padx=10
        )

        self.refresh_button = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.load_expenses
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
            command=self.delete_expense
        )

        self.delete_button.pack(
            side="left",
            padx=10
        )

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update Expense",
            command=self.update_expense
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
            "Expense",
            "Category",
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
            self.select_expense
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.load_expenses()

    def load_expenses(self):

        # Clear existing rows
        for row in self.tree.get_children():

            self.tree.delete(row)

        sql = """
        SELECT
            expense_id,
            expense_name,
            category,
            amount,
            expense_date
        FROM Expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC
        """

        try:

            self.expense_manager.cursor.execute(
                sql,
                (self.expense_manager.user["user_id"],)
            )

            expenses = self.expense_manager.cursor.fetchall()

            for expense in expenses:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        expense[0],
                        expense[1],
                        expense[2],
                        f"₹{expense[3]:.2f}",
                        expense[4].strftime("%d-%b-%Y")
                    )
                )

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def add_expense(self):

        name = self.name_entry.get().strip()

        category = self.category.get()

        amount = self.amount_entry.get().strip()

        description = self.description_entry.get().strip()

        if not name:

            CTkMessagebox(
                title="Error",
                message="Expense name is required.",
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
        INSERT INTO Expenses
        (user_id, expense_name, category, amount, expense_date, description)
        VALUES (%s, %s, %s, %s, NOW(), %s)
        """

        values = (
            self.expense_manager.user["user_id"],
            name,
            category,
            amount,
            description
        )

        try:

            self.expense_manager.cursor.execute(sql, values)

            self.expense_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Expense added successfully!",
                icon="check"
            )

            self.load_expenses()

            self.refresh_dashboard()

            self.clear_form()

        except Exception as e:

            print(e)

    def clear_form(self):

        self.name_entry.delete(0, "end")

        self.category.set("Food")

        self.amount_entry.delete(0, "end")

        self.description_entry.delete(0, "end")

        self.selected_expense_id = None

        self.tree.selection_remove(
            self.tree.selection()
        )

        self.update_button.configure(
            state="disabled"
        )

    def delete_expense(self):

        selected = self.tree.selection()

        if not selected:

            CTkMessagebox(
                title="Warning",
                message="Please select an expense first.",
                icon="warning"
            )
            return

        expense_id = self.tree.item(selected[0])["values"][0]

        response = CTkMessagebox(
            title="Confirm Delete",
            message="Are you sure you want to delete this expense?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete"
        )

        if response.get() != "Delete":
            return

        sql = """
        DELETE FROM Expenses
        WHERE expense_id = %s
        """

        try:

            self.expense_manager.cursor.execute(
                sql,
                (expense_id,)
            )

            self.expense_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Expense deleted successfully!",
                icon="check"
            )

            self.load_expenses()

            self.refresh_dashboard()

            self.clear_form()

        except Exception as e:

            print(e)

    def select_expense(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        self.selected_expense_id = values[0]

        self.update_button.configure(
            state="normal"
        )

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, values[1])

        self.category.set(values[2])

        amount = values[3].replace("₹", "").replace(",", "")
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, amount)

        sql = """
        SELECT description
        FROM Expenses
        WHERE expense_id = %s
        """

        self.expense_manager.cursor.execute(
            sql,
            (self.selected_expense_id,)
        )

        description = self.expense_manager.cursor.fetchone()[0]

        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, description)
        
    def update_expense(self):

        if self.selected_expense_id is None:

            print("Select an expense first.")
            return

        name = self.name_entry.get().strip()
        category = self.category.get()
        amount = self.amount_entry.get().strip()
        description = self.description_entry.get().strip()

        if not name:

            print("Expense name is required.")
            return

        try:

            amount = float(amount)

        except ValueError:

            print("Invalid amount.")
            return

        sql = """
        UPDATE Expenses
        SET
            expense_name = %s,
            category = %s,
            amount = %s,
            description = %s
        WHERE expense_id = %s
        """

        values = (
            name,
            category,
            amount,
            description,
            self.selected_expense_id
        )

        try:

            self.expense_manager.cursor.execute(sql, values)

            self.expense_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Expense updated successfully!",
                icon="check"
            )

            self.load_expenses()

            self.refresh_dashboard()

            self.clear_form()

            self.selected_expense_id = None

        except Exception as e:

            print(e)
