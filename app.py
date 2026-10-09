import streamlit as st
import plotly.express as px

from src.data_processing import load_business_data, clean_business_data
from src.prediction import forecast_revenue, evaluate_forecast_model
from src.recommendations import generate_recommendations
from src.assistant import business_assistant
from src.smart_alerts import generate_smart_alerts


# ============================================================
# PAGE CONFIGURATION
# ============================================================

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


# ============================================================
# FILE UPLOAD
# ============================================================

st.header("📂 Upload Business Data")

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


if uploaded_file is None:
    st.info(
        "Upload a CSV or Excel file to start "
        "analyzing your business data."
    )

else:
    try:
        # ----------------------------------------------------
        # LOAD AND CLEAN DATA
        # ----------------------------------------------------

        df = load_business_data(uploaded_file)
        df = clean_business_data(df)

        if df.empty:
            st.warning(
                "The uploaded file contains no usable records."
            )
            st.stop()

        st.success("Business data uploaded successfully! ✅")

        # Check required columns before running the dashboard.
        required_columns = [
            "date",
            "product",
            "revenue",
            "expense",
            "quantity_sold"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            st.error(
                "Your file is missing required columns: "
                + ", ".join(missing_columns)
            )
            st.info(
                "Please check your column names and upload "
                "a file containing the required business fields."
            )
            st.stop()

        # ----------------------------------------------------
        # BUSINESS KPIs
        # ----------------------------------------------------

        total_revenue = df["revenue"].sum()
        total_expenses = df["expense"].sum()
        total_profit = total_revenue - total_expenses
        total_units = df["quantity_sold"].sum()

        profit_margin = (
            (total_profit / total_revenue) * 100
            if total_revenue > 0
            else 0
        )

        st.subheader("📊 Business Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💰 Revenue", f"₹{total_revenue:,.0f}")

        with col2:
            st.metric("💸 Expenses", f"₹{total_expenses:,.0f}")

        with col3:
            st.metric("📈 Profit", f"₹{total_profit:,.0f}")

        with col4:
            st.metric("📦 Units Sold", f"{total_units:,.0f}")

        # ----------------------------------------------------
        # BUSINESS TRENDS
        # ----------------------------------------------------

        st.subheader("📈 Business Trends")

        trend_data = df.copy()
        import pandas as pd

        trend_data["date"] = pd.to_datetime(
            trend_data["date"],
            errors="coerce"
        )

        trend_data = trend_data.dropna(subset=["date"])

        if not trend_data.empty:
            trend_data = (
                trend_data.groupby("date", as_index=False)[
                    ["revenue", "expense"]
                ].sum()
            )

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

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(
                "No valid dates were found for the business trend chart."
            )

        # ----------------------------------------------------
        # SMART BUSINESS ALERTS
        # ----------------------------------------------------

        st.subheader("🚨 Smart Business Alerts")

        alerts = generate_smart_alerts(df)

        for alert in alerts:
            level = alert["level"]

            with st.container(border=True):
                if level == "critical":
                    st.error(f"🔴 {alert['title']}")
                elif level == "warning":
                    st.warning(f"⚠️ {alert['title']}")
                elif level == "success":
                    st.success(f"✅ {alert['title']}")
                else:
                    st.info(f"ℹ️ {alert['title']}")

                st.write(alert["message"])
                st.caption(
                    f"Recommended action: {alert['recommendation']}"
                )

        # ----------------------------------------------------
        # PRODUCT PERFORMANCE
        # ----------------------------------------------------

        st.subheader("🛍️ Product Performance")

        product_data = df.groupby(
            "product",
            as_index=False
        )[
            ["revenue", "expense", "quantity_sold"]
        ].sum()

        product_data["profit"] = (
            product_data["revenue"] - product_data["expense"]
        )

        if not product_data.empty:
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

            # ------------------------------------------------
            # AUTOMATIC BUSINESS INSIGHTS
            # ------------------------------------------------

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
                    f"📉 **Lowest Revenue Product:** "
                    f"{lowest_revenue_product}"
                )
                st.success(
                    f"📦 **Best-Selling Product:** "
                    f"{best_selling_product}"
                )

        # ----------------------------------------------------
        # REVENUE FORECAST
        # ----------------------------------------------------

        st.subheader("🔮 Revenue Forecast")

        forecast_data = forecast_revenue(df, days=7)

        if forecast_data is not None and not forecast_data.empty:
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
        else:
            st.warning(
                "A revenue forecast could not be generated "
                "from the available data."
            )

        # ----------------------------------------------------
        # MODEL PERFORMANCE
        # ----------------------------------------------------

        st.subheader("📏 Forecast Model Performance")

        mae = evaluate_forecast_model(df)

        if mae is not None:
            st.metric(
                "Mean Absolute Error (MAE)",
                f"₹{mae:,.0f}"
            )

            st.caption(
                "MAE represents the average absolute difference "
                "between predicted and actual revenue."
            )

        # ----------------------------------------------------
        # PROFIT MARGIN AND EXPENSE SUMMARY
        # ----------------------------------------------------

        st.subheader("📌 Financial Summary")

        if profit_margin < 10:
            st.error(
                f"⚠️ Low profit margin: {profit_margin:.1f}%"
            )
        elif profit_margin < 20:
            st.warning(
                f"⚠️ Profit margin needs attention: "
                f"{profit_margin:.1f}%"
            )
        else:
            st.success(
                f"✅ Recorded profit margin: {profit_margin:.1f}%"
            )

        expense_ratio = (
            (total_expenses / total_revenue) * 100
            if total_revenue > 0
            else 0
        )

        if expense_ratio > 70:
            st.warning(
                f"💸 Expenses are {expense_ratio:.1f}% of revenue."
            )
        else:
            st.info(
                f"💰 Expenses represent {expense_ratio:.1f}% "
                "of revenue."
            )

        # ----------------------------------------------------
        # BUSINESS RECOMMENDATIONS
        # ----------------------------------------------------

        st.subheader("🤖 BizPilot Recommendations")

        recommendations = generate_recommendations(
            total_revenue,
            total_expenses,
            total_profit,
            product_data,
            profit_margin
        )

        for recommendation in recommendations:
            st.info(recommendation)

        # ----------------------------------------------------
        # BIZPILOT AI ASSISTANT
        # ----------------------------------------------------

        st.subheader("🤖 BizPilot AI")

        st.write(
            "Ask questions about your business data "
            "and get data-driven answers."
        )

        question = st.text_input(
            "Ask BizPilot about your business",
            placeholder=(
                "Example: Which product makes the most profit?"
            ),
            key="bizpilot_question"
        )

        if question.strip():
            answer = business_assistant(
                question,
                df,
                total_revenue,
                total_expenses,
                total_profit,
                profit_margin,
                product_data,
                forecast_data,
                recommendations
            )

            st.success(answer)

        # ----------------------------------------------------
        # DATA PREVIEW
        # ----------------------------------------------------

        with st.expander("📋 View Uploaded Data"):
            st.dataframe(df, use_container_width=True)

            st.caption(
                f"BizPilot detected {df.shape[0]} rows and "
                f"{df.shape[1]} columns."
            )
    except Exception as e:
        st.error(f"Error processing the file: {e}")
