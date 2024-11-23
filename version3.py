import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.title("Personal Expense Tracker")

# Initialize session state to store data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# Sidebar inputs for expense entry
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form"):
    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0.01, format="%.2f", step=0.01)
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")

# Add new expense to the data
if submitted:
    new_expense = {"Date": date, "Amount": amount, "Category": category, "Description": description}
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_expense])], ignore_index=True)
    st.success("Expense added!")

# Display the expenses table
st.subheader("Expense History")
if not st.session_state.data.empty:
    st.write(st.session_state.data)
else:
    st.info("No expenses added yet!")

# Visualizations
if not st.session_state.data.empty:
    # Group data by category for pie chart
    category_summary = st.session_state.data.groupby("Category")["Amount"].sum()

    # Pie chart for expense breakdown
    st.subheader("Expense Breakdown by Category")
    fig1, ax1 = plt.subplots()
    ax1.pie(category_summary, labels=category_summary.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig1)

    # Line chart for expenses over time
    st.subheader("Expense Trend Over Time")
    st.session_state.data["Date"] = pd.to_datetime(st.session_state.data["Date"])
    trend_data = st.session_state.data.groupby("Date")["Amount"].sum().reset_index()
    st.line_chart(trend_data.rename(columns={"Amount": "Total Expense"}).set_index("Date"))
else:
    st.info("Add some expenses to see visualizations!")

# Run the app

