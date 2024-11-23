import streamlit as st
import pandas as pd
import plotly.express as px
import os

# File to store finance data
DATA_FILE = "finance_data.csv"

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Date", "Type", "Amount", "Category"]).to_csv(DATA_FILE, index=False)

# Load data
def load_data():
    return pd.read_csv(DATA_FILE)

# Save data
def save_data(new_entry):
    data = load_data()
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)

# App Title and Sidebar Navigation
st.title("💰 Personal Finance Tracker")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Input Data", "Visualize Spending", "Savings Goal Tracker"])

# Home Page
if page == "Home":
    st.header("Welcome to the Personal Finance Tracker!")
    st.write("""
    This app helps you:
    - Input and categorize your income and expenses.
    - Visualize spending habits with interactive charts.
    - Track your progress toward financial goals.
    
    Use the sidebar to navigate through the app's features.
    """)

# Input Data Page
if page == "Input Data":
    st.header("📊 Input Income and Expenses")

    # Select entry type
    entry_type = st.radio("Select Entry Type:", ["Income", "Expense"])
    amount = st.number_input(f"Enter {entry_type} Amount:", min_value=0.0, format="%.2f")
    category = st.text_input(f"{entry_type} Category (e.g., Salary, Rent, Food):")
    date = st.date_input("Select Date")

    # Save entry
    if st.button("Save Entry"):
        if amount > 0 and category:
            new_entry = pd.DataFrame({
                "Date": [date],
                "Type": [entry_type],
                "Amount": [amount],
                "Category": [category]
            })
            save_data(new_entry)
            st.success(f"{entry_type} entry saved successfully!")
        else:
            st.error("Please fill in all fields before saving.")

# Visualization Page
if page == "Visualize Spending":
    st.header("📈 Spending Visualization")

    # Load data
    data = load_data()

    if data.empty:
        st.warning("No data available. Please add some entries first!")
    else:
        # Convert date and extract month
        data["Date"] = pd.to_datetime(data["Date"])
        data["Month"] = data["Date"].dt.to_period("M").astype(str)

        # Monthly spending trend
        st.subheader("Monthly Spending Trend")
        monthly_spending = data[data["Type"] == "Expense"].groupby("Month")["Amount"].sum()
        fig_monthly = px.bar(x=monthly_spending.index, y=monthly_spending.values,
                             labels={"x": "Month", "y": "Spending"},
                             title="Monthly Spending Trend")
        st.plotly_chart(fig_monthly)

        # Category-wise spending
        st.subheader("Category-wise Spending")
        category_spending = data[data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
        fig_category = px.pie(values=category_spending.values, names=category_spending.index,
                              title="Spending by Category")
        st.plotly_chart(fig_category)

# Savings Goal Tracker Page
if page == "Savings Goal Tracker":
    st.header("🏦 Savings Goal Tracker")

    # Input goal amount
    goal_amount = st.number_input("Set your savings goal:", min_value=0.0, format="%.2f")

    # Calculate savings
    data = load_data()
    total_income = data[data["Type"] == "Income"]["Amount"].sum()
    total_expenses = data[data["Type"] == "Expense"]["Amount"].sum()
    current_savings = total_income - total_expenses

    # Display progress
    progress = (current_savings / goal_amount) * 100 if goal_amount > 0 else 0
    st.progress(progress / 100)
    st.write(f"Current Savings: ${current_savings:.2f}")
    st.write(f"Goal Progress: {progress:.2f}%")

    if progress >= 100:
        st.success("🎉 Congratulations! You've reached your savings goal!")
    elif progress > 0:
        st.info("You're on your way! Keep saving to reach your goal.")
    else:
        st.warning("Start saving to meet your financial goal.")

# Footer
st.sidebar.info("Built with 💻 by Streamlit Enthusiast")

