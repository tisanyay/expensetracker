from pages.Dining import dashboard
from Overall import transaction_history

shopping_transactions = transaction_history[transaction_history["Category"]=="Shopping"]

dashboard(shopping_transactions)