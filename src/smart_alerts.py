
import pandas as pd


def generate_smart_alerts(df):
    """
    Generate business alerts from uploaded business data.
    Supports revenue, expenses, profit, and inventory alerts
    when the required columns are available.
    """

    alerts = []

    if df is None or df.empty:
        return [{
            "level": "info",
            "title": "No business data",
            "message": "Upload a business file to generate alerts.",
            "recommendation": "Upload a CSV or Excel file containing your business records."
        }]

    data = df.copy()

    # Normalize column names
    data.columns = (
        data.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Convert supported numeric columns safely
    numeric_columns = [
        "revenue", "sales", "expenses", "expense",
        "profit", "quantity", "stock",
        "stock_quantity", "quantity_in_stock",
        "quantity_sold"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )
    # --------------------------------------------------
    # 1. LOW STOCK ALERT
    # --------------------------------------------------
    stock_column = next(
        (
            col for col in [
                "stock_quantity",
                "quantity_in_stock",
                "stock_on_hand",
                "current_stock",
                "available_stock",
                "stock"
            ]
            if col in data.columns
        ),
        None
    )

    if stock_column and "product" in data.columns:
        stock_data = data.dropna(subset=[stock_column]).copy()

        stock_data[stock_column] = pd.to_numeric(
            stock_data[stock_column],
            errors="coerce"
        )

        stock_data = stock_data.dropna(subset=[stock_column])

        # Negative stock should be handled as a separate warning.
        low_stock = stock_data[
            (stock_data[stock_column] >= 0)
            & (stock_data[stock_column] <= 5)
        ]

        for _, row in low_stock.iterrows():
            alerts.append({
                "level": "warning",
                "title": f"Low stock: {row['product']}",
                "message": (
                    f"Only {row[stock_column]:g} units "
                    "are recorded in stock."
                ),
                "recommendation": (
                    "Verify the physical stock and consider "
                    "reordering if demand is expected."
                )
            })

    # --------------------------------------------------
    # 2. NEGATIVE STOCK / DATA WARNING
    # --------------------------------------------------
    if stock_column:
        negative_stock = data[
            data[stock_column] < 0
        ].dropna(subset=[stock_column])

        for _, row in negative_stock.iterrows():
            product = row.get("product", "Unknown product")

            alerts.append({
                "level": "critical",
                "title": f"Check stock record: {product}",
                "message": (
                    f"The recorded {stock_column} is negative "
                    f"({row[stock_column]:g})."
                ),
                "recommendation": (
                    "Check for data-entry errors or stock "
                    "transactions that have not been recorded correctly."
                )
            })

    # --------------------------------------------------
    # 3. EXPENSE ALERT
    # --------------------------------------------------
    expense_column = next(
        (
            col for col in ["expenses", "expense"]
            if col in data.columns
        ),
        None
    )

    revenue_column = next(
        (
            col for col in ["revenue", "sales"]
            if col in data.columns
        ),
        None
    )

    if expense_column and revenue_column:
        valid = data[
            [expense_column, revenue_column]
        ].dropna()

        total_expenses = valid[expense_column].sum()
        total_revenue = valid[revenue_column].sum()

        if total_revenue > 0:
            expense_ratio = (
                total_expenses / total_revenue
            ) * 100

            if expense_ratio > 80:
                alerts.append({
                    "level": "warning",
                    "title": "High expense ratio",
                    "message": (
                        f"Recorded expenses are "
                        f"{expense_ratio:.1f}% of recorded revenue."
                    ),
                    "recommendation": (
                        "Review major expense categories and "
                        "confirm that the records cover the same period."
                    )
                })

        if (valid[expense_column] < 0).any():
            alerts.append({
                "level": "warning",
                "title": "Check negative expenses",
                "message": (
                    "Some expense records have negative values."
                ),
                "recommendation": (
                    "Check whether these represent refunds or "
                    "data-entry errors before interpreting totals."
                )
            })

    # --------------------------------------------------
    # 4. PROFIT WARNING
    # --------------------------------------------------
    if "profit" in data.columns:
        valid_profit = data["profit"].dropna()

        if not valid_profit.empty and valid_profit.sum() < 0:
            alerts.append({
                "level": "critical",
                "title": "Business loss detected",
                "message": (
                    f"Total recorded profit is "
                    f"{valid_profit.sum():,.2f}, below zero."
                ),
                "recommendation": (
                    "Review revenue, costs, and the reporting period "
                    "before deciding what action to take."
                )
            })

    # --------------------------------------------------
    # 5. NEGATIVE REVENUE WARNING
    # --------------------------------------------------
    if revenue_column:
        if (data[revenue_column].dropna() < 0).any():
            alerts.append({
                "level": "warning",
                "title": "Check negative revenue records",
                "message": (
                    "Some revenue values are negative."
                ),
                "recommendation": (
                    "Verify whether these represent refunds, "
                    "returns, or incorrect entries."
                )
            })

    # --------------------------------------------------
    # 6. REVENUE AND EXPENSE TREND ALERTS
    # --------------------------------------------------
    if (
        "date" in data.columns
        and revenue_column
        and expense_column
    ):
        trend_data = data.copy()

        trend_data["date"] = pd.to_datetime(
            trend_data["date"],
            errors="coerce"
        )

        trend_data = trend_data.dropna(
            subset=["date"]
        )

        if trend_data["date"].nunique() >= 4:
            daily = (
                trend_data.groupby("date")[
                    [revenue_column, expense_column]
                ]
                .sum()
                .sort_index()
            )

            midpoint = len(daily) // 2
            earlier = daily.iloc[:midpoint]
            later = daily.iloc[midpoint:]

            earlier_revenue = earlier[revenue_column].sum()
            later_revenue = later[revenue_column].sum()

            earlier_expense = earlier[expense_column].sum()
            later_expense = later[expense_column].sum()

            if earlier_revenue > 0:
                revenue_change = (
                    (later_revenue - earlier_revenue)
                    / earlier_revenue
                ) * 100

                if revenue_change <= -20:
                    alerts.append({
                        "level": "warning",
                        "title": "Revenue decline detected",
                        "message": (
                            f"Revenue fell by "
                            f"{abs(revenue_change):.1f}% "
                            "between the earlier and later "
                            "recorded periods."
                        ),
                        "recommendation": (
                            "Review product-wise sales, pricing, "
                            "and customer demand to investigate "
                            "the decline."
                        )
                    })

            if earlier_expense > 0:
                expense_change = (
                    (later_expense - earlier_expense)
                    / earlier_expense
                ) * 100

                if expense_change >= 20:
                    alerts.append({
                        "level": "warning",
                        "title": "Expense increase detected",
                        "message": (
                            f"Recorded expenses increased by "
                            f"{expense_change:.1f}% between "
                            "the earlier and later periods."
                        ),
                        "recommendation": (
                            "Identify which products or expense "
                            "categories contributed to the increase."
                        )
                    })
    # --------------------------------------------------
    # 6. NO ALERTS
    # --------------------------------------------------
    if not alerts:
        alerts.append({
            "level": "success",
            "title": "No immediate alerts",
            "message": (
                "No issues were detected by the available checks."
            ),
            "recommendation": (
                "Continue monitoring your records. This does not "
                "guarantee that every business risk has been detected."
            )
        })

    return alerts
