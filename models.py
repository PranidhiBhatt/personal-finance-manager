"""
models.py
Contains all data models used in the project.
"""


class User:

    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password


class Expense:

    def __init__(self, expense_type, category, amount, expense_date, description, user_id):

        self.expense_type = expense_type
        self.category = category
        self.amount = amount
        self.expense_date = expense_date
        self.description = description
        self.user_id = user_id

class Income:

    def __init__(
        self,
        source,
        amount,
        income_date,
        user_id
    ):

        self.source = source
        self.amount = amount
        self.income_date = income_date
        self.user_id = user_id

class Budget:

    def __init__(
        self,
        budget_id,
        user_id,
        category,
        budget_amount,
        month
    ):

        self.budget_id = budget_id
        self.user_id = user_id
        self.category = category
        self.budget_amount = budget_amount
        self.month = month
