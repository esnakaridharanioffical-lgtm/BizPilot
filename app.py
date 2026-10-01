import streamlit as st

st.set_page_config(
    page_title="BizPilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 BizPilot")
st.subheader("AI-Powered Business Intelligence Platform")

st.write(
    "Transform your business data into meaningful insights, "
    "predictions, alerts, and actionable recommendations."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Revenue", "₹0")

with col2:
    st.metric("Expenses", "₹0")

with col3:
    st.metric("Profit", "₹0")

st.info(
    "Upload your business data to start analyzing your business performance."
)