import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("Personal Finance Tracker Dashboard")

# File upload
uploaded_file = st.file_uploader(
    "Upload your expense CSV",
    type=["csv"]
)

# Run only after file is uploaded
if uploaded_file:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Show uploaded data
    st.subheader("Expense Data")
    st.write(df)

    # Spending by category
    st.subheader("Spending by Category")
    category_sum = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_sum)

    # Monthly trend
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    monthly = df.groupby("Month")["Amount"].sum()

    st.subheader("Monthly Spending Trend")
    st.line_chart(monthly)

    # Budget alert
    st.subheader("Budget Alert")

    budget = st.number_input(
        "Set Monthly Budget",
        value=5000
    )

    total_spent = df["Amount"].sum()

    if total_spent > budget:
        st.error("⚠ Budget exceeded!")
    else:
        st.success("✅ Within budget")

    # Pie chart
    st.subheader("Expense Breakdown")

    fig = px.pie(
        df,
        names="Category",
        values="Amount",
        title="Expense Breakdown"
    )

    st.plotly_chart(fig)

    # Category filter
    st.subheader("Filter by Category")

    selected_category = st.selectbox(
        "Choose a category",
        df["Category"].unique()
    )

    filtered_df = df[df["Category"] == selected_category]

    st.write(filtered_df)