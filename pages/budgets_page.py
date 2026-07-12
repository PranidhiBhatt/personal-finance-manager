import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class BudgetPage(ctk.CTkFrame):

    def __init__(self, parent, budget_manager, refresh_dashboard):

        super().__init__(parent)

        self.budget_manager = budget_manager
        self.refresh_dashboard = refresh_dashboard
        self.selected_budget_id = None

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Budget Management",
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
        # Category
        # ==========================

        ctk.CTkLabel(
            form,
            text="Category"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.category = ctk.CTkComboBox(
            form,
            values=[
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Education",
                "Healthcare",
                "Travel",
                "Other"
            ],
            width=300
        )

        self.category.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        # ==========================
        # Budget Amount
        # ==========================

        ctk.CTkLabel(
            form,
            text="Budget Amount"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.amount_entry = ctk.CTkEntry(
            form,
            width=300
        )

        self.amount_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=15
        )

        # ==========================
        # Month
        # ==========================

        ctk.CTkLabel(
            form,
            text="Month"
        ).grid(
            row=2,
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
            row=2,
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

        self.add_button = ctk.CTkButton(
            button_frame,
            text="Add Budget",
            command=self.add_budget         
        )

        self.add_button.pack(
            side="left",
            padx=10
        )

        self.refresh_button = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.load_budget
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
            command=self.delete_budget
        )

        self.delete_button.pack(
            side="left",
            padx=10
        )

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update Budget",
            command=self.update_budget
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
            "Category",
            "Budget",
            "Month"
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
            self.select_budget
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.load_budget()

    def load_budget(self):

        # Clear existing rows
        for row in self.tree.get_children():

            self.tree.delete(row)

        sql = """
        SELECT
        budget_id,
        category,
        budget_amount,
        month
        FROM Budgets
        WHERE user_id=%s
        ORDER BY budget_id DESC
        """

        try:

            self.budget_manager.cursor.execute(
                sql,
                (self.budget_manager.user["user_id"],)
            )

            budgets = self.budget_manager.cursor.fetchall()

            for budget in budgets:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        budget[0],
                        budget[1],
                        f"₹{budget[2]:,.2f}",
                        budget[3]
                    )
                )

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def add_budget(self):

        category = self.category.get().strip()
        amount = self.amount_entry.get().strip()
        month = self.month_entry.get().strip()

        if not category:

            CTkMessagebox(
                title="Error",
                message="Please select a category.",
                icon="cancel"
            )
            return

        if not month:

            if len(month) != 7 or month[4] != "-":

                CTkMessagebox(
                    title="Error",
                    message="Month must be in YYYY-MM format.",
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
        INSERT INTO Budgets
        (
            user_id,
            category,
            budget_amount,
            month
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (

            self.budget_manager.user["user_id"],
            category,
            amount,
            month

        )

        try:

            self.budget_manager.cursor.execute(
                sql,
                values
            )

            self.budget_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Budget added successfully!",
                icon="check"
            )

            self.load_budget()
            self.refresh_dashboard()
            self.clear_form()

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def clear_form(self):

        self.category.set("Food")

        self.amount_entry.delete(0, "end")

        self.month_entry.delete(0, "end")

        self.selected_budget_id = None

        self.update_button.configure(
            state="disabled"
        )

    def delete_budget(self):

        if self.selected_budget_id is None:

            CTkMessagebox(
                title="Warning",
                message="Please select a budget first.",
                icon="warning"
            )

            return

        sql = """
        DELETE FROM Budgets
        WHERE budget_id=%s
        """

        try:

            self.budget_manager.cursor.execute(
                sql,
                (
                    self.selected_budget_id,
                )
            )

            self.budget_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Budget deleted successfully!",
                icon="check"
            )

            self.load_budget()

            self.refresh_dashboard()

            self.clear_form()

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )

    def select_budget(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_budget_id = values[0]

        self.update_button.configure(
            state="normal"
        )

        self.category.set(values[1])

        amount = values[2].replace(
            "₹",
            ""
        ).replace(
            ",",
            ""
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.amount_entry.insert(
            0,
            amount
        )

        self.month_entry.delete(
            0,
            "end"
        )

        self.month_entry.insert(
            0,
            values[3]
        )
        
    def update_budget(self):

        if self.selected_budget_id is None:

            CTkMessagebox(
                title="Warning",
                message="Please select a budget first.",
                icon="warning"
            )

            return

        category = self.category.get().strip()
        amount = self.amount_entry.get().strip()
        month = self.month_entry.get().strip()

        if not month:
            
            if len(month) != 7 or month[4] != "-":

                CTkMessagebox(
                    title="Error",
                    message="Month must be in YYYY-MM format.",
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
        UPDATE Budgets
        SET
            category=%s,
            budget_amount=%s,
            month=%s
        WHERE budget_id=%s
        """

        values = (

            category,
            amount,
            month,
            self.selected_budget_id

        )

        try:

            self.budget_manager.cursor.execute(
                sql,
                values
            )

            self.budget_manager.connection.commit()

            CTkMessagebox(
                title="Success",
                message="Budget updated successfully!",
                icon="check"
            )

            self.load_budget()

            self.refresh_dashboard()

            self.clear_form()

        except Exception as e:

            CTkMessagebox(
                title="Database Error",
                message=str(e),
                icon="cancel"
            )
