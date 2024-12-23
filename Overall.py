import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dataframe_formatters
from math import ceil
from datetime import date
from datetime import datetime

# st.set_page_config(layout="wide")

cols = st.columns(6)
this_month = cols[0].button("This Month")
all_time = cols[1].button("All Time")

st.write("# Transactions analysis from June to December 2024")

transaction_history_1 = pd.read_csv("./transaction_history_csv/sep-dec.csv")
transaction_history_2 = pd.read_csv("./transaction_history_csv/jun-sep.csv")
transaction_history = pd.concat([transaction_history_1, transaction_history_2])

# transaction_history = transaction_history[transaction_history["Reference"] == "UMC-S"]
transaction_history["Transaction Date"] = pd.to_datetime(transaction_history["Transaction Date"])
transaction_history["Debit Amount"] = transaction_history["Debit Amount"].replace({' ': np.nan})
transaction_history["Debit Amount"] = transaction_history["Debit Amount"].astype(float)
transaction_history["Credit Amount"] = transaction_history["Credit Amount"].replace({' ': np.nan})
transaction_history["Credit Amount"] = transaction_history["Credit Amount"].astype(float)
transaction_history["Date"] = transaction_history["Transaction Date"].dt.strftime('%b %d')
transaction_history["Month"] = transaction_history["Transaction Date"].dt.strftime('%m %b')
transaction_history["Transaction Ref1"] = transaction_history["Transaction Ref1"].fillna("")
transaction_history["Transaction Ref2"] = transaction_history["Transaction Ref2"].fillna("")
transaction_history["Transaction Ref3"] = transaction_history["Transaction Ref3"].fillna("")
transaction_history["Vendor"] = transaction_history["Transaction Ref1"] + ' ' + transaction_history["Transaction Ref2"] + ' ' + transaction_history["Transaction Ref3"]
transaction_history = transaction_history[transaction_history["Reference"] != "ITR"]

# F&B vendors list
with open("./restaurants.txt") as restaurants:
    lines = restaurants.readlines()

    restaurant_list = []
    for line in lines:
        line = [dataframe_formatters.remove_special_characters(e) for e in line.split(", ")]
        restaurant_list.extend(line)

    restaurant_list = list(set(restaurant_list))

# Transport, transfers, salary, and medical lists
transport_list = ["bus", "grab"]
transfer_list = ["kwynnzie"]
salary_list = ["mindef", "saf", "gov"]
medical_list = ["polyclinic", "clinic"]

# Vendor group dictionary
vendor_groups = {
    "F&B": restaurant_list,
    "Transport": transport_list,
    "Transfers": transfer_list,
    "Salary": salary_list,
    "Medical": medical_list
}

# Transportation vendors list
transaction_history["Category"] = transaction_history["Vendor"].apply(lambda x: dataframe_formatters.categorize_vendors(x, vendor_groups))

transaction_history_copy = transaction_history
if this_month:
    transaction_history = transaction_history[transaction_history["Month"] == datetime.today().strftime("%m %b")]

if all_time:
    transaction_history = transaction_history_copy


col1, col2 = st.columns(2)

df = transaction_history[transaction_history["Debit Amount"].notna()]
df = df[["Category", "Debit Amount"]].groupby("Category").agg(["mean", "median", "sum", "count"]).round(2)
col1.dataframe(df)

df = transaction_history[transaction_history["Debit Amount"].notna()][["Category", "Debit Amount"]].groupby("Category").sum()
pie_chart_fig = px.pie(df, values="Debit Amount", names=df.index, height=300, width=300)
col2.plotly_chart(pie_chart_fig)

st.plotly_chart(px.box(transaction_history, x="Category", y="Debit Amount"))

df = transaction_history[transaction_history["Debit Amount"].notna()][["Month", "Category", "Debit Amount"]].groupby(["Month", "Category"]).sum()
st.line_chart(data=df.reset_index(), x="Month", y="Debit Amount", color="Category")

df = transaction_history
df["In/Out"] = df["Category"].apply(lambda x: "In" if x == "Salary" else "Out")
df["Amount"] = df["Debit Amount"]
df["Amount"] = df["Amount"].fillna(-df["Credit Amount"])
df.loc[df["Category"]=="Salary", "Amount"] *= -1

df = df[["Month", "In/Out", "Amount"]].groupby(["Month", "In/Out"]).sum()

fig = px.bar(df.reset_index(), x="Month", y="Amount", color="In/Out", barmode="group", color_discrete_map={"In": "rgb(68, 170, 153)", "Out": "rgb(204, 102, 119)"})
st.plotly_chart(fig)


st.write("## Calculate goals to reach 6k by June 2026")
savings = st.number_input("Input current savings: ")
salary = st.number_input("input salary: ")

def months_diff(start, end):
    return ceil((end - start).days / 30) 

if savings and salary:
    months_left = months_diff(datetime.today(), datetime(2026, 6, 3))
    money_to_save = 6000 - savings

    money_to_save_each_month = money_to_save / months_left
    money_to_save_each_month = round(money_to_save_each_month)
    money_to_spend = round((salary - money_to_save_each_month), 2)
    money_to_save_each_month = str(money_to_save_each_month)
    st.write("#### You'll have to save at least \$" + money_to_save_each_month + " each month to reach your $6k goal by June 2026.")
    st.write("This gives you $" + str(money_to_spend) + " each month to spend.")
    
    st.write("Transport fixed at $80")
    minus_transport = money_to_spend - 80
    st.write("40\% for shopping -> $" + str(0.4*minus_transport))
    st.write("35\% for transfers -> $" + str(0.35*minus_transport))
    st.write("15\% for dining -> $" + str(0.15*minus_transport))