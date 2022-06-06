import csv
from classes.budget import Budget

import pandas as pd
import plotly.express as plot

DEFAULT_MESSAGE = "--==**  Command Line Budget App  **==--\n" \
                  "Select an option from below\n" \
                  "1. Update Monthly Income\n" \
                  "2. Add Expense(s)\n" \
                  "3. Remove Expense(s)\n" \
                  "4. View Budget\n" \
                  "5. Quit\n"

EXPENSES_MAIN_MENU = "What kind of expense would you like to add?\n" \
                     "1. Food\n" \
                     "2. Living\n" \
                     "3. Fun\n" \
                     "4. Savings\n" \
                     "5. Misc\n" \
                     "6. ** Go back to Main Menu **\n"

EXPENSES_LAST_MENU = "Select an option from below:\n" \
                     "1. Finish adding expenses. (Main Menu)\n" \
                     "2. Add a new expense\n"

REMOVE_EXPENSE_MENU = "Select an option from below:\n" \
                      "1. List all expenses\n" \
                      "2. Remove expense by ID\n" \
                      "3. Remove all expenses\n" \
                      "4. Main Menu\n"

EXPENSE_TYPES = [
    "NONE",
    "Food",
    "Living",
    "Fun",
    "Savings",
    "Misc",
]


def main_loop():
    while True:
        user_input = input(DEFAULT_MESSAGE)

        if user_input == "1":
            setup_monthly_income()
        if user_input == "2":
            add_expenses_menu()
        if user_input == "3":
            remove_expense_menu()
        if user_input == "4":
            open_budget_graph()
        if user_input == "5":
            exit()
        if user_input == "6":
            calculatePercentages()


def add_expenses_menu():
    setup_step = 0
    while setup_step < 3:
        if setup_step == 0:
            user_input = input(EXPENSES_MAIN_MENU)
            if not user_input.isnumeric() or (int(user_input) > 6 or int(user_input) < 0):
                # Not a valid entry
                continue
            if user_input == "6":
                # They selected to go back to the main menu, so break this loop
                break
            # Legal entry - so update - next step in menu
            Budget.current_expense_type = EXPENSE_TYPES[int(user_input)]
            setup_step += 1
        if setup_step == 1:
            modified_string = "Enter the amount of money the expense {type} will be\n".format(
                type=Budget.current_expense_type)
            user_input = input(modified_string)
            if not user_input.isnumeric():
                continue
            Budget.current_expense_amount = user_input
            setup_step += 1
        if setup_step == 2:
            modified_string = "You're attempting to set an expense valued at {type} ${amount}".format(
                type=Budget.current_expense_type, amount=Budget.current_expense_amount)
            modified_string += ".\nTo confirm enter 'confirm', otherwise enter any key to retry\n"
            user_input = input(modified_string)
            if user_input == "confirm":
                # Tell the obj to update to the main expenses list (not saved to csv yet)
                Budget.add_current_expense(Budget)
                setup_step += 1
            else:
                setup_step -= 1
        # We need an option to add another expense (setting setup-step to 0 or 1 to repeat) or finalize to add to csv
        if setup_step == 3:
            user_input = input(EXPENSES_LAST_MENU)
            if int(user_input) == 1:
                for expense in Budget.expenses:
                    # Add to CSV
                    update_expenses(expense)
                # Since we updated the CSV, we need to clear our list so new ones can be added without duplication
                Budget.reset_expenses(Budget)
                break
            if int(user_input) == 2:
                setup_step = 0


def remove_expense_menu():
    while True:
        user_input = input(REMOVE_EXPENSE_MENU)
        if user_input == "1":
            display_all_expenses()
        if user_input == "2":
            user_input = input("Input ID number of the expense you'd like to remove\n")
            if not remove_expense_by_id(int(user_input)):
                print("Could not remove expense by that ID.\n")
            update_expense_list()
        if user_input == "3":
            clear_expense_list()
        if user_input == "4":
            break


def open_budget_graph():
    expense_file = pd.read_csv('data/expenses.csv')
    expense_type = expense_file['expense_type']
    expense_amount = expense_file['expense_amount']
    expense_fig = plot.bar(expense_file, x=expense_type, y=expense_amount, labels={
        'expense_type': 'Expense Types', 'expense_amount': 'Expense Costs'
    })
    expense_fig.show()


def setup_monthly_income():
    setup_step = 0
    while setup_step < 2:
        if setup_step == 0:
            user_input = input("Input your monthly income (Round to the nearest dollar)\n")
            if user_input.isnumeric():
                Budget.monthly_income = user_input
                setup_step += 1
            else:
                print("Invalid amount was enter. Round to the nearest dollar.")

        if setup_step == 1:
            modified_string = "You're attempting to set your monthly income at ${income}".format(
                income=Budget.monthly_income)
            modified_string += ".\nTo confirm enter 'confirm', otherwise enter any key to retry\n"
            user_input = input(modified_string)
            if user_input == "confirm":
                update_monthly_income(Budget.monthly_income)
                break
            setup_step -= 1


def update_monthly_income(monthly_income):
    """
    The user should provide an amount (rounded to the nearest dollar) and then we make a dict out of it,
    then we store it in the CSV in a manner which only updates, not appends
    :param monthly_income: int
    :return: void
    """
    monthly_income_dict = {'monthly_income': monthly_income}
    with open('data/monthly_income.csv', 'w', newline='') as file:
        field_names = ['monthly_income']
        writer = csv.DictWriter(file, field_names)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(monthly_income_dict)


def update_expenses(data_as_dict):
    with open('data/expenses.csv', 'a+', newline='') as file:
        field_names = ['expense_type', 'expense_amount']
        writer = csv.DictWriter(file, field_names)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data_as_dict)


def display_all_expenses():
    with open('data/expenses.csv', newline='') as file:
        rows_in_file = csv.DictReader(file)
        output = "** All Expenses **\n"
        counter = 0
        for row in rows_in_file:
            output += f"ID: {counter}\n{row['expense_type']}: ${row['expense_amount']}\n-----------\n"
            counter += 1
            Budget.loaded_expenses.append(row)
        return print(output)


def clear_expense_list():
    with open('data/expenses.csv', 'w', newline='') as file:
        field_names = ['expense_type', 'expense_amount']
        writer = csv.DictWriter(file, field_names)
        if file.tell() == 0:
            writer.writeheader()


def remove_expense_by_id(expense_id):
    amount_of_expenses = len(Budget.loaded_expenses)
    if expense_id < 0 or expense_id > amount_of_expenses:
        return False
    del Budget.loaded_expenses[expense_id]
    return True


def update_expense_list():
    with open('data/expenses.csv', 'w', newline='') as file:
        field_names = ['expense_type', 'expense_amount']
        writer = csv.DictWriter(file, field_names)
        if file.tell() == 0:
            writer.writeheader()
        for expense in Budget.loaded_expenses:
            writer.writerow(expense)


def calculatePercentages():
    display_all_expenses()
    #     For now we use this function just to load our list
    list_of_expenses = Budget.loaded_expenses
    food = 0
    living = 0
    misc = 0
    saving = 0
    fun = 0
    for expense in list_of_expenses:
        expense_type = expense['expense_type']
        expense_amount = expense['expense_amount']
        if expense_type == 'Food':
            food += expense_amount
        if expense_type == 'Living':
            living += expense_amount
        if expense_type == 'Savings':
            saving += expense_amount
        if expense_type == 'Fun':
            fun += expense_amount
        if expense_type == 'Misc':
            misc += expense_amount
    print(fun, food, living, misc, saving)
