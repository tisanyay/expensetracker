# import streamlit as st
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import dataframe_formatters 

# st.write("# Transactions analysis from June to December 2024")

# transaction_history_1 = pd.read_csv("./transaction_history_csv/sep-dec.csv")
# transaction_history_2 = pd.read_csv("./transaction_history_csv/jun-sep.csv")
# transaction_history = pd.concat([transaction_history_1, transaction_history_2])

# # transaction_history = transaction_history[transaction_history["Reference"] == "UMC-S"]
# transaction_history["Transaction Date"] = pd.to_datetime(transaction_history["Transaction Date"])
# transaction_history["Debit Amount"] = transaction_history["Debit Amount"].replace({' ': np.nan})
# transaction_history["Debit Amount"] = transaction_history["Debit Amount"].astype(float)
# transaction_history["Date"] = transaction_history["Transaction Date"].dt.strftime('%b %d')
# transaction_history["Month"] = transaction_history["Transaction Date"].dt.strftime('%m %b')
# transaction_history["Vendor"] = transaction_history["Transaction Ref1"].fillna(transaction_history["Transaction Ref2"])
# transaction_history = transaction_history[transaction_history["Reference"] != "ITR"]

# # F&B vendors list
# with open("./restaurants.txt") as restaurants:
#     lines = restaurants.readlines()

#     restaurant_list = []
#     for line in lines:
#         line = [dataframe_formatters.remove_special_characters(e) for e in line.split(", ")]
#         restaurant_list.extend(line)

#     restaurant_list = list(set(restaurant_list))

# # Transport, transfers, salary, and medical lists
# transport_list = ["bus", "grab"]
# transfer_list = ["paynow", "transfer", "ref", "bank", "revolut"]
# salary_list = ["mindef", "saf"]
# medical_list = ["polyclinic", "clinic"]

# # Vendor group dictionary
# vendor_groups = {
#     "F&B": restaurant_list,
#     "Transport": transport_list,
#     "Transfers": transfer_list,
#     "Salary": salary_list,
#     "Medical": medical_list
# }

# # Transportation vendors list
# transaction_history["Category"] = transaction_history["Vendor"].apply(lambda x: dataframe_formatters.categorize_vendors(x, vendor_groups))
# output_directory = "../transaction_history_csv/out.csv"
# transaction_history["Category"].value_counts()

# df = dataframe_formatters.get_shopping_and_fb_categories(transaction_history[transaction_history["Category"]=="F&B"])
# summary_df = df[['Month', 'Debit Amount']].groupby('Month').agg(['mean', 'median', 'sum', 'count']).round(2)

# # st.dataframe(transaction_history)
# st.dataframe(summary_df)

# fig, ax = plt.subplots()
# df = dataframe_formatters.get_shopping_and_fb_categories(transaction_history)
# month_axis_ordering = sorted(transaction_history["Month"].unique())
# sns.boxplot(data=df, x="Month", y="Debit Amount", order=month_axis_ordering, ax=ax, showfliers=False)

# st.write(fig)


from pages.Dining import dashboard
from Overall import transaction_history

shopping_transactions = transaction_history[transaction_history["Category"]=="Shopping"]

dashboard(shopping_transactions)