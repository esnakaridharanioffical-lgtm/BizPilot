import streamlit as st
import plotly.express as px

from src.data_processing import load_business_data, clean_business_data
from src.prediction import forecast_revenue, evaluate_forecast_model

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

# File Upload
st.header("📂 Upload Business Data")

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    try:
        # Load data
        df = load_business_data(uploaded_file)

        # Clean data
        df = clean_business_data(df)

        st.success("Business data uploaded successfully! ✅")

        # Business KPIs
        total_revenue = df["revenue"].sum()
        total_expenses = df["expense"].sum()
        total_profit = total_revenue - total_expenses
        total_units = df["quantity_sold"].sum()

        st.subheader("📊 Business Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💰 Revenue", f"₹{total_revenue:,.0f}")

        with col2:
            st.metric("💸 Expenses", f"₹{total_expenses:,.0f}")

        with col3:
            st.metric("📈 Profit", f"₹{total_profit:,.0f}")

        with col4:
            st.metric("📦 Units Sold", f"{total_units:,}")

        # Business Trends
        st.subheader("📈 Business Trends")

        trend_data = df.groupby("date", as_index=False)[
            ["revenue", "expense"]
        ].sum()

        trend_data["profit"] = (
            trend_data["revenue"] - trend_data["expense"]
        )

        fig = px.line(
            trend_data,
            x="date",
            y=["revenue", "expense", "profit"],
            markers=True,
            title="Revenue, Expenses & Profit Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
                # Product Performance
        st.subheader("🛍️ Product Performance")

        product_data = df.groupby(
            "product",
            as_index=False
        )[["revenue", "expense", "quantity_sold"]].sum()

        product_data["profit"] = (
            product_data["revenue"] - product_data["expense"]
        )

        fig_product = px.bar(
            product_data,
            x="product",
            y="revenue",
            title="Revenue by Product",
            text_auto=True
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True
        )
                # Automatic Business Insights
        st.subheader("💡 Business Insights")

        top_revenue_product = product_data.loc[
            product_data["revenue"].idxmax(), "product"
        ]

        lowest_revenue_product = product_data.loc[
            product_data["revenue"].idxmin(), "product"
        ]

        top_profit_product = product_data.loc[
            product_data["profit"].idxmax(), "product"
        ]

        best_selling_product = product_data.loc[
            product_data["quantity_sold"].idxmax(), "product"
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"🏆 **Top Revenue Product:** {top_revenue_product}"
            )

            st.info(
                f"💰 **Top Profit Product:** {top_profit_product}"
            )

        with col2:
            st.warning(
                f"📉 **Lowest Revenue Product:** {lowest_revenue_product}"
            )

            st.success(
                f"📦 **Best-Selling Product:** {best_selling_product}"
            )
                    # Revenue Forecast
        st.subheader("🔮 Revenue Forecast")

        forecast_data = forecast_revenue(df, days=7)

        fig_forecast = px.line(
            forecast_data,
            x="date",
            y="predicted_revenue",
            markers=True,
            title="Predicted Revenue for the Next 7 Days"
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )

        st.info(
            "🔮 BizPilot uses historical revenue trends "
            "to estimate the next 7 days."
        )
                # Model Evaluation
        st.subheader("📏 Forecast Model Performance")

        mae = evaluate_forecast_model(df)

        st.metric(
            "Mean Absolute Error (MAE)",
            f"₹{mae:,.0f}"
        )

        st.caption(
            "MAE represents the average absolute difference "
            "between predicted and actual revenue."
        )

                # Smart Alerts
        st.subheader("🚨 Smart Alerts")

        profit_margin = (total_profit / total_revenue) * 100

        if profit_margin < 10:
            st.error(
                f"⚠️ Low profit margin detected: {profit_margin:.1f}%"
            )
        elif profit_margin < 20:
            st.warning(
                f"⚠️ Profit margin needs attention: {profit_margin:.1f}%"
            )
        else:
            st.success(
                f"✅ Healthy profit margin: {profit_margin:.1f}%"
            )

        expense_ratio = (total_expenses / total_revenue) * 100

        if expense_ratio > 70:
            st.warning(
                f"💸 Expenses are high: {expense_ratio:.1f}% of revenue."
            )
        else:
            st.info(
                f"💰 Expenses represent {expense_ratio:.1f}% of revenue."
            )

        if lowest_revenue_product:
            st.warning(
                f"📉 Watch product performance: "
                f"{lowest_revenue_product} has the lowest revenue."
            )

        # Data Preview
        st.subheader("📋 Data Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.info(
            f"BizPilot detected {df.shape[0]} rows and "
            f"{df.shape[1]} columns."
        )

    except Exception as e:
        st.error(f"Error processing the file: {e}")

else:
    st.info(
        "Upload a CSV or Excel file to start analyzing your business data."
    )