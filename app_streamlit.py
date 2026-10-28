import streamlit as st
import pandas as pd
import numpy as np

# ----------------- 1. PAGE TITLE & HEADER -----------------
st.set_page_config(page_title="AI & Analytics Dashboard", page_icon="📊", layout="centered")

st.title("📊 E-Commerce AI & Analytics Dashboard")
st.write("Pure Python se bana hua interactive web app (Powered by Streamlit)")


# ----------------- 2. USER INPUTS (Sliders, Dropdowns) -----------------
st.header("👤 Customer Churn Prediction")

# Streamlit ke widgets (Zero HTML/CSS!)
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Customer Age", min_value=18, max_value=70, value=35)
    support_calls = st.number_input("Customer Support Calls", min_value=0, max_value=10, value=2)

with col2:
    balance = st.number_input("Account Balance (₹)", min_value=1000, max_value=200000, value=50000)
    city = st.selectbox("Select City", ["Delhi", "Mumbai", "Bangalore"])


# ----------------- 3. LIVE PREDICTION LOGIC -----------------
if st.button("🚀 Predict Customer Churn"):
    # Chhoti si logic: High support calls + high age = Churn risk
    if support_calls >= 4:
        st.error(f"⚠️ HIGH RISK! Customer from {city} has an 82% chance of leaving the bank!")
    else:
        st.success(f"✅ SAFE! Customer from {city} is happy and will stay (Loyalty Score: 95%).")


# ----------------- 4. LIVE ANALYTICS DATA & CHARTS -----------------
st.divider()
st.header("📈 Monthly Revenue Chart")

# Sample revenue data
chart_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [45000, 52000, 48000, 61000, 75000, 89000]
}).set_index("Month")

# 1-line interactive line chart!
st.line_chart(chart_data)

# Data Table
st.subheader("Raw Sales Data")
st.dataframe(chart_data.T)