from Overall import transaction_history
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression

st.write("# *Dining* transactions analysis from June to December 2024")

dining_transactions = transaction_history[transaction_history["Category"]=="F&B"]

def dashboard(transactions):
    today_datetime = datetime.today()
    first_day_of_the_month = today_datetime.replace(day=1)
    last_month_datetime = first_day_of_the_month - timedelta(days=1)
    first_day_of_last_month = last_month_datetime.replace(day=1)
    last_last_month_datetime = first_day_of_last_month - timedelta(days=1)

    last_month_transactions = transactions[transactions["Month"]==last_month_datetime.strftime("%m %b")]
    last_last_month_transactions = transactions[transactions["Month"]==last_last_month_datetime.strftime("%m %b")]


    mean = round(last_month_transactions["Debit Amount"].mean())
    median = round(last_month_transactions["Debit Amount"].median())
    sum = round(last_month_transactions["Debit Amount"].sum())
    count = round(last_month_transactions["Debit Amount"].count())

    last_mean = round(last_last_month_transactions["Debit Amount"].mean())
    last_median = round(last_last_month_transactions["Debit Amount"].median())
    last_sum = round(last_last_month_transactions["Debit Amount"].sum())
    last_count = round(last_last_month_transactions["Debit Amount"].count())

    delta_mean = mean - last_mean
    delta_median = median - last_median
    delta_sum = sum - last_sum
    delta_count = count - last_count


    st.write(" ")
    st.write("#### Last month")
    cols = st.columns(4)

    cols[0].metric(label="Mean", value=mean, delta=delta_mean, delta_color="inverse")
    cols[1].metric(label="Median", value=median, delta=delta_median, delta_color="inverse")
    cols[2].metric(label="Sum", value=sum, delta=delta_sum, delta_color="inverse")
    cols[3].metric(label="Count", value=count, delta=delta_count, delta_color="inverse")

    matrix = transactions[['Month', 'Debit Amount']].groupby('Month').agg(['mean', 'median', 'sum', 'count'])
    matrix.columns = matrix.columns.droplevel()
    st.dataframe(matrix.transpose())
    matrix = matrix[:-1]

    trace1 = go.Box(x=transactions["Month"], y=transactions["Debit Amount"], name="Spending distribution")

    df = transactions[transactions["Debit Amount"].notna()][["Month", "Debit Amount"]].groupby(["Month"]).sum().reset_index()

    trace2 = go.Line(x=df["Month"], y=df["Debit Amount"], marker_color="red", name="Total spent")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2, secondary_y=True)
    fig.update_xaxes(autorange="reversed")
    fig.update_layout(title_text="Spending distribution against total spent for each month")

    st.plotly_chart(fig)

    X = matrix["count"].values[:, np.newaxis]
    y = matrix["sum"].values

    model = LinearRegression()
    model.fit(X, y)

    trace1 = go.Scatter(x=matrix["count"], y=model.predict(X), mode="lines")
    trace2 = go.Scatter(x=matrix["count"], y=matrix["sum"], mode="markers")

    fig = make_subplots()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_layout(title_text="Scatter plot of total spending on dining against count of transactions with best fit line")
    st.plotly_chart(fig)

    coef = round(model.coef_[0], 2)
    intercept = round(model.intercept_, 2)

    if intercept > 0:
        st.latex('sum = ' + str(coef) + ' \cdot count + ' + str(intercept))
    else:
        st.latex('sum = ' + str(coef) + ' \cdot count - ' + str(-intercept))



    budget = st.number_input("Enter in budget for dining:", key=np.random)

    if budget:
        dine_out_count = (budget - intercept) / coef
        st.markdown("You can dine out at an estimated " + str(round(dine_out_count, 1)) + " times a month")

dashboard(dining_transactions)