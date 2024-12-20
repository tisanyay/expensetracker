from pprint import pprint
import pandas as pd
import datetime

"""
    Expense Tracker App
        Tracks expenses using AI and machine learning to make better financial decisions.
"""

"""
class Expense:
    def __init__(self, pandas_datetime_object, description, dollar_amount_sgd, category):
        self.date = pandas_datetime_object # date class
        self.description = description 
        self.amount = dollar_amount_sgd
        self.category = category
    
    def __repr__(self):
        return f"{self.date.strftime('%B %d')}\t\t{self.description}\t\t{self.amount}"

        

class ExpenseHistory:
    @staticmethod
    def __init__(self):
        self.expenses = []

    @staticmethod
    def add_expense(self, expense_object):
        self.expenses.append(expense_object)
    
    @staticmethod
    def add_expense_sheet(parser_object):
        pass

    @staticmethod
    def view_expenses(self):
        pprint(self.expenses)
"""

def dbs_csv_to_df(csv_file_directory):
    df = pd.read_csv(csv_file_directory, skiprows=7)
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

    return df

transaction_history = pd.DataFrame(columns=['Transaction Date', 'Transaction Posting Date',
       'Transaction Description', 'Transaction Category', 'Payment Mode',
       'Transaction Status', 'Debit Amount', 'Credit Amount'])

csv_file_directory = "./transaction_history_csv/November.csv"

transaction_history = pd.concat([transaction_history, dbs_csv_to_df(csv_file_directory)])

print(transaction_history)