import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dataframe_formatters
import io
from math import ceil
from datetime import date
from datetime import datetime

# st.set_page_config(layout="wide")

cols = st.columns(6)
this_month = cols[0].button("This Month")
all_time = cols[1].button("All Time")


transaction_file = "./transaction_history_csv/cleaned_transaction_history.csv"

transaction_history = pd.read_csv(transaction_file)

uploaded_file = st.file_uploader("Input transaction file")


if uploaded_file:
    with st.spinner("waiting"):
        initial_length = transaction_history.shape[0]

        uploaded_file = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        transaction_history = dataframe_formatters.append_uploaded_transaction_history(uploaded_file, transaction_history)
        dataframe_formatters.output_csv(transaction_history, "./transaction_history_csv.cleaned_transaction_history.csv")

        final_length = transaction_history.shape[0]
        st.write("Rows added: " + str(final_length - initial_length))


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
st.bar_chart(data=df.reset_index(), x="Month", y="Debit Amount", color="Category")

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
    
    st.write("Transport fixed at $100")
    minus_transport = money_to_spend - 100
    st.write("50\% for shopping -> $" + str(0.5*minus_transport))
    st.write("20\% for transfers -> $" + str(0.2*minus_transport))
    st.write("30\% for dining -> $" + str(0.3*minus_transport))

def normalize(arr):
    return pd.Series([i/sum(arr) for i in arr])

def change_label(month):
    return sum(df[df["Month"]==month].values[0][1:])

matrix = transaction_history[transaction_history["Debit Amount"].notna()]
matrix = matrix[['Month', 'Category', 'Debit Amount']].groupby(['Month', "Category"]).agg(['mean', 'median', 'sum', 'count'])
matrix.columns = matrix.columns.droplevel()
matrix = matrix["sum"].reset_index().pivot(index="Month", columns="Category", values="sum")
if 'Medical' in matrix.columns:
    matrix = matrix.drop("Medical", axis=1).fillna(0)
cols = matrix.columns

matrix1 = matrix.apply(lambda x: normalize(x), axis=1)
matrix1.columns = cols
matrix1 = matrix1.reset_index()
df = matrix.reset_index()
matrix1 = pd.melt(matrix1, value_vars=cols, id_vars=["Month"])
matrix1["Month"] = matrix1["Month"].apply(change_label)

st.plotly_chart(px.scatter(matrix1, y="value", x="Month", color="Category", title="Percentage of total expenditure spent on each category against total expenditure of each month"))

st.dataframe(transaction_history[["Transaction Date", "Category", "Vendor", "Debit Amount"]])