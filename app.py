import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('your_filename.csv')

# Clean column names
df.columns = df.columns.str.strip().str.title()

# Fix date format
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df.dropna(subset=['Order Date'], inplace=True)

# Sidebar filters
st.sidebar.header("Filter Data")

# Category filter
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

# Date range filter
min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Apply filters
filtered_df = df[
    (df['Category'].isin(selected_categories)) &
    (df['Order Date'] >= pd.to_datetime(start_date)) &
    (df['Order Date'] <= pd.to_datetime(end_date))
]

# Title
st.title("📊 Sales Dashboard")

# Summary metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum() if 'Profit' in filtered_df.columns else 0
num_orders = filtered_df.shape[0]

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Number of Orders", num_orders)

# Line chart: Daily sales
daily_sales = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()

st.subheader("📈 Daily Sales Over Time")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(daily_sales['Order Date'], daily_sales['Sales'], color='teal')
ax1.set_title("Sales Over Time")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sales")
st.pyplot(fig1)

# Bar chart: Sales by category
category_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values()

st.subheader("📊 Sales by Category")
fig2, ax2 = plt.subplots()
category_sales.plot(kind='barh', ax=ax2, color='skyblue')
ax2.set_xlabel("Sales")
ax2.set_ylabel("Category")
ax2.set_title("Total Sales by Category")
st.pyplot(fig2)

# Optional: Profit by category (if exists)
if 'Profit' in filtered_df.columns:
    profit_by_cat = filtered_df.groupby('Category')['Profit'].sum().sort_values()

    st.subheader("💰 Profit by Category")
    fig3, ax3 = plt.subplots()
    profit_by_cat.plot(kind='barh', ax=ax3, color='orange')
    ax3.set_xlabel("Profit")
    ax3.set_ylabel("Category")
    ax3.set_title("Total Profit by Category")
    st.pyplot(fig3)

# Insights section
st.subheader("🧠 Insights")
st.markdown(f"""
- The highest sales occurred between **{daily_sales['Order Date'].max().date()}** and **{daily_sales['Order Date'].min().date()}**.
- **{category_sales.idxmax()}** is the best-selling category.
- There are **{num_orders}** total orders in the selected period.
""")
