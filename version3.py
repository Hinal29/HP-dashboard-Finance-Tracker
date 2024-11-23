import streamlit as st
import pandas as pd
import plotly.express as px
import os

# App Title
st.title("💰 Personal Finance Tracker")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to:", ["Home", "Input Data", "Visualize Spending", "Savings Goal Tracker"])

# Initialize data file
DATA_FILE = "finance_data.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Date", "Type", "Amount", "Category"]).to_csv(DATA_FILE, index=False)

# Load data
def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(new_entry):
    data = load_data()
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)

# Input Data
if page == "Input Data":
    st.header("📊 Input Income and Expenses")
    
    # Choose type of data to input
    entry_type = st.radio("Select Entry Type:", ["Income", "Expense"])
    amount = st.number_input(f"Enter {entry_type} Amount:", min_value=0.0, format="%.2f")
    category = st.text_input(f"{entry_type} Category (e.g., Salary, Rent, Food):")
    date = st.date_input("Date")
    
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
            st.error("Please fill all fields before saving.")

# Visualize Spending
if page == "Visualize Spending":
    st.header("📈 Spending Visualization")
    data = load_data()
    
    if data.empty:
        st.warning("No data available. Please add some entries first!")
    else:
        # Monthly trend
        data["Date"] = pd.to_datetime(data["Date"])
        data["Month"] = data["Date"].dt.to_period("M").astype(str)
        monthly_summary = data[data["Type"] == "Expense"].groupby("Month")["Amount"].sum()
        
        st.subheader("Monthly Spending Trend")
        fig_monthly = px.line(x=monthly_summary.index, y=monthly_summary.values, labels={"x": "Month", "y": "Spending"},
                              title="Monthly Spending")
        st.plotly_chart(fig_monthly)
        
        # Category-wise spending
        st.subheader("Category-wise Spending")
        category_summary = data[data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
        fig_category = px.pie(values=category_summary.values, names=category_summary.index,
                              title="Spending by Category")
        st.plotly_chart(fig_category)

# Savings Goal Tracker
if page == "Savings Goal Tracker":
    st.header("🏦 Savings Goal Tracker")
    
    # Input goal and current savings
    goal_amount = st.number_input("Set your savings goal:", min_value=0.0, format="%.2f")
    data = load_data()
    current_savings = data[data["Type"] == "Income"]["Amount"].sum() - data[data["Type"] == "Expense"]["Amount"].sum()
    
    # Calculate progress
    progress = (current_savings / goal_amount) * 100 if goal_amount > 0 else 0
    st.progress(progress / 100)
    st.write(f"Current Savings: ${current_savings:.2f}")
    st.write(f"Goal Progress: {progress:.2f}%")
    
    if progress >= 100:
        st.success("Congratulations! You've achieved your savings goal!")
    elif progress > 0:
        st.info("Keep going! You're on track to reach your goal.")
    else:
        st.warning("Start saving to meet your goal!")

# Home Page
if page == "Home":
    st.header("Welcome to Personal Finance Tracker!")
    st.write("""
    This app helps you:
    - Input and categorize your income and expenses.
    - Visualize spending trends with interactive charts.
    - Track your progress toward savings goals.
    
    Use the sidebar to navigate between features.
    """)

# Footer
st.sidebar.info("Designed with 💻 by Your Name")
