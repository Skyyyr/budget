class Budget:
    monthly_income = 0
    expenses = []
    current_expense_type = ""
    current_expense_amount = 0
    loaded_expenses = []

    def __init__(self):
        pass

    def __str__(self):
        pass

    def add_current_expense(self):
        expense_dict = {'expense_type':self.current_expense_type, 'expense_amount': self.current_expense_amount}
        self.expenses.append(expense_dict)

    def reset_expenses(self):
        self.expenses = []
