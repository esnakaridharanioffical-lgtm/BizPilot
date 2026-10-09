import pandas as pd


def business_assistant(
    question,
    df,
    total_revenue,
    total_expenses,
    total_profit,
    profit_margin,
    product_data,
    forecast_data=None,
    recommendations=None
):
    """
    Answer business questions using BizPilot's actual business data.
    """

    question = question.lower().strip()

    # =========================================================
    # PRODUCT QUESTIONS
    # =========================================================

    # ---------------------------------------------------------
    # PRODUCT COMPARISON
    # ---------------------------------------------------------

    if (
        "compare" in question
        and len(product_data["product"]) >= 2
    ):

        matched_products = []

        for product in product_data["product"]:
            if str(product).lower() in question:
                matched_products.append(product)

        matched_products = list(dict.fromkeys(matched_products))

        if len(matched_products) < 2:
            return (
                "Please mention two product names so I can "
                "compare their performance."
            )

        product_1 = matched_products[0]
        product_2 = matched_products[1]

        row_1 = product_data[
            product_data["product"] == product_1
        ].iloc[0]

        row_2 = product_data[
            product_data["product"] == product_2
        ].iloc[0]

        revenue_1 = row_1["revenue"]
        revenue_2 = row_2["revenue"]

        expense_1 = row_1["expense"]
        expense_2 = row_2["expense"]

        profit_1 = row_1["profit"]
        profit_2 = row_2["profit"]

        units_1 = row_1["quantity_sold"]
        units_2 = row_2["quantity_sold"]

        margin_1 = (
            (profit_1 / revenue_1) * 100
            if revenue_1 > 0
            else 0
        )

        margin_2 = (
            (profit_2 / revenue_2) * 100
            if revenue_2 > 0
            else 0
        )

        return (
            f"📊 Product Comparison\n\n"
            f"🔹 {product_1}\n"
            f"Revenue: ₹{revenue_1:,.2f}\n"
            f"Units sold: {units_1:,.0f}\n"
            f"Expenses: ₹{expense_1:,.2f}\n"
            f"Profit: ₹{profit_1:,.2f}\n"
            f"Profit margin: {margin_1:.1f}%\n\n"
            f"🔹 {product_2}\n"
            f"Revenue: ₹{revenue_2:,.2f}\n"
            f"Units sold: {units_2:,.0f}\n"
            f"Expenses: ₹{expense_2:,.2f}\n"
            f"Profit: ₹{profit_2:,.2f}\n"
            f"Profit margin: {margin_2:.1f}%"
        )

    # ---------------------------------------------------------
    # HIGHEST PROFIT PRODUCT
    # ---------------------------------------------------------

    if (
        "most profit" in question
        or "highest profit" in question
    ):

        index = product_data["profit"].idxmax()

        product = product_data.loc[index, "product"]
        profit = product_data.loc[index, "profit"]

        return (
            f"{product} is your highest-profit product, "
            f"generating ₹{profit:,.2f} in profit."
        )

    # ---------------------------------------------------------
    # LOWEST REVENUE PRODUCT
    # ---------------------------------------------------------

    if (
        "lowest revenue" in question
        or "least revenue" in question
    ):

        index = product_data["revenue"].idxmin()

        product = product_data.loc[index, "product"]
        revenue = product_data.loc[index, "revenue"]

        return (
            f"{product} has the lowest revenue at "
            f"₹{revenue:,.2f}."
        )

    # ---------------------------------------------------------
    # BEST SELLING PRODUCT
    # ---------------------------------------------------------

    if (
        "best selling" in question
        or "best-selling" in question
        or "most sold" in question
        or "sells the most" in question
        or "sell the most" in question
    ):

        index = product_data["quantity_sold"].idxmax()

        product = product_data.loc[index, "product"]
        units = product_data.loc[index, "quantity_sold"]

        return (
            f"{product} is your best-selling product "
            f"with {units:,.0f} units sold."
        )

    # ---------------------------------------------------------
    # HIGHEST REVENUE PRODUCT
    # ---------------------------------------------------------

    if (
        "top revenue" in question
        or "highest revenue" in question
    ):

        index = product_data["revenue"].idxmax()

        product = product_data.loc[index, "product"]
        revenue = product_data.loc[index, "revenue"]

        return (
            f"{product} generates the highest revenue "
            f"at ₹{revenue:,.2f}."
        )

    # =========================================================
    # PRODUCT PERFORMANCE DIAGNOSIS
    # =========================================================

    # ---------------------------------------------------------
    # PRODUCT PERFORMING WELL
    # ---------------------------------------------------------

    if (
        "why" in question
        and "performing well" in question
    ):
        matched_product = None

        for product in product_data["product"]:
            if str(product).lower() in question:
                matched_product = product
                break

        if matched_product is None:
            return (
                "Please mention the product name so I can "
                "analyze its performance."
            )

        product_row = product_data[
            product_data["product"] == matched_product
        ].iloc[0]

        revenue = product_row["revenue"]
        expense = product_row["expense"]
        profit = product_row["profit"]
        units = product_row["quantity_sold"]

        margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        return (
            f"{matched_product} is performing well with "
            f"₹{revenue:,.2f} in revenue, "
            f"{units:,.0f} units sold, and "
            f"₹{profit:,.2f} in profit. "
            f"Its product-level profit margin is "
            f"{margin:.1f}%, indicating that it is generating "
            f"substantial profit relative to its revenue."
        )



        # =========================================================
    # EXPENSE TREND ANALYSIS
    # =========================================================

    if (
        ("expense" in question or "expenses" in question)
        and (
            "trend" in question
            or "how are expenses changing" in question
            or "how have expenses changed" in question
        )
    ):

        try:
            trend_df = df.copy()

            trend_df["date"] = pd.to_datetime(
                trend_df["date"]
            )

            daily_expense = (
                trend_df
                .groupby("date")
                .agg(
                    expense=("expense", "sum"),
                    revenue=("revenue", "sum")
                )
                .sort_index()
            )

            if len(daily_expense) < 2:
                return (
                    "I need data from at least two different dates "
                    "to analyze your expense trend."
                )

            first_expense = daily_expense["expense"].iloc[0]
            last_expense = daily_expense["expense"].iloc[-1]

            expense_change = last_expense - first_expense

            expense_change_pct = (
                (expense_change / first_expense) * 100
                if first_expense != 0
                else 0
            )

            if expense_change > 0:
                return (
                    f"Your expense trend is increasing. "
                    f"Expenses rose from ₹{first_expense:,.2f} "
                    f"to ₹{last_expense:,.2f}, an increase of "
                    f"{expense_change_pct:.1f}%. "
                    "This indicates that your costs are currently "
                    "moving upward and should be monitored closely."
                )

            elif expense_change < 0:
                return (
                    f"Your expense trend is decreasing. "
                    f"Expenses fell from ₹{first_expense:,.2f} "
                    f"to ₹{last_expense:,.2f}, a decrease of "
                    f"{abs(expense_change_pct):.1f}%. "
                    "This indicates that your overall cost level "
                    "has improved over the recorded period."
                )

            else:
                return (
                    "Your expense trend is relatively stable. "
                    "There is no significant change between the "
                    "first and latest recorded expense values."
                )

        except Exception:
            return (
                "I couldn't analyze the expense trend because "
                "the expense or date data could not be processed."
            )



    # =========================================================
    # EXPENSE INTELLIGENCE
    # =========================================================

    if (
        ("expense" in question or "expenses" in question)
        and (
            "why" in question
            or "increasing" in question
            or "increase" in question
            or "decreasing" in question
            or "decrease" in question
            or "performance" in question
            or "performing" in question
            or "how is" in question
            or "how are" in question
            or "doing" in question
            or "happening" in question
        )
        and "trend" not in question
    ):

        try:
            expense_df = df.copy()
            expense_df["date"] = pd.to_datetime(expense_df["date"])

            daily_data = (
                expense_df
                .groupby("date")
                .agg(
                    revenue=("revenue", "sum"),
                    expense=("expense", "sum")
                )
                .sort_index()
            )

            if len(daily_data) < 2:
                return (
                    "I need data from at least two different dates "
                    "to analyze your expense performance."
                )

            if len(daily_data) >= 14:
                first_dates = daily_data.index[:7]
                latest_dates = daily_data.index[-7:]
            else:
                midpoint = len(daily_data) // 2
                first_dates = daily_data.index[:midpoint]
                latest_dates = daily_data.index[midpoint:]

            first_period = expense_df[
                expense_df["date"].isin(first_dates)
            ]
            latest_period = expense_df[
                expense_df["date"].isin(latest_dates)
            ]

            first_expense = first_period["expense"].sum()
            latest_expense = latest_period["expense"].sum()
            first_revenue = first_period["revenue"].sum()
            latest_revenue = latest_period["revenue"].sum()

            expense_change = latest_expense - first_expense

            expense_change_pct = (
                (expense_change / abs(first_expense)) * 100
                if first_expense != 0
                else 0
            )

            first_expense_ratio = (
                (first_expense / first_revenue) * 100
                if first_revenue > 0
                else 0
            )

            latest_expense_ratio = (
                (latest_expense / latest_revenue) * 100
                if latest_revenue > 0
                else 0
            )

            ratio_change = (
                latest_expense_ratio - first_expense_ratio
            )

            if expense_change_pct > 2:
                direction = "increased"
            elif expense_change_pct < -2:
                direction = "decreased"
            else:
                direction = "remained relatively stable"

            # Product-level expense drilldown.
            first_product = (
                first_period
                .groupby("product")["expense"]
                .sum()
            )

            latest_product = (
                latest_period
                .groupby("product")["expense"]
                .sum()
            )

            product_expense = pd.concat(
                [first_product, latest_product],
                axis=1
            ).fillna(0)

            product_expense.columns = [
                "first_expense",
                "latest_expense"
            ]

            product_expense["change"] = (
                product_expense["latest_expense"]
                - product_expense["first_expense"]
            )

            rising_costs = (
                product_expense[
                    product_expense["change"] > 0
                ]
                .sort_values("change", ascending=False)
                .head(3)
            )

            largest_expense_product = (
                latest_product.idxmax()
                if len(latest_product) > 0
                else None
            )

            largest_expense_value = (
                latest_product.max()
                if len(latest_product) > 0
                else 0
            )

            if direction == "increased":
                if ratio_change > 1:
                    pressure = (
                        "expenses increased and are taking a larger "
                        "share of revenue"
                    )
                elif latest_revenue < first_revenue:
                    pressure = (
                        "expenses increased while revenue decreased"
                    )
                else:
                    pressure = (
                        "higher operating or product-level costs"
                    )
            elif direction == "decreased":
                pressure = (
                    "overall expenses decreased, improving the cost position"
                )
            else:
                pressure = (
                    "relatively stable costs compared with revenue"
                )

            if len(rising_costs) > 0:
                cost_lines = []
                for product, row in rising_costs.iterrows():
                    cost_lines.append(
                        f"• {product}: "
                        f"₹{row['change']:,.2f} higher expense"
                    )
                cost_text = "\n".join(cost_lines)
            else:
                cost_text = (
                    "• No product showed a meaningful increase "
                    "in expense."
                )

            if direction == "increased":
                if len(rising_costs) > 0:
                    action = (
                        "Investigate the products with the largest "
                        "expense increases and compare their costs "
                        "with revenue and profit contribution. "
                        "If detailed cost data is available, review "
                        "supplier prices, purchasing quantities, and "
                        "operating costs before changing sales volume."
                    )
                else:
                    action = (
                        "Review major operating and purchasing costs "
                        "and compare them with revenue and profit before "
                        "the next business cycle."
                    )
            elif direction == "decreased":
                if len(rising_costs) > 0:
                    action = (
                        "Maintain the improved cost position, but investigate "
                        "the products with notable expense increases and "
                        "compare their costs with revenue and profit contribution."
                    )
                else:
                    action = (
                        "Maintain the improved cost position while monitoring "
                        "major expense contributors and their impact on revenue "
                        "and profit."
                    )
            else:
                action = (
                    "Costs are relatively stable. Monitor the largest "
                    "expense contributors and look for opportunities "
                    "to improve the expense-to-revenue ratio."
                )

            return (
                f"💸 Expense Intelligence\n\n"
                f"Your expenses {direction} by "
                f"{abs(expense_change_pct):.1f}% between the "
                f"comparison periods.\n\n"
                f"First period expenses: "
                f"₹{first_expense:,.2f}\n"
                f"Latest period expenses: "
                f"₹{latest_expense:,.2f}\n"
                f"Expense-to-revenue ratio: "
                f"{first_expense_ratio:.1f}% → "
                f"{latest_expense_ratio:.1f}% "
                f"({ratio_change:+.1f} percentage points)\n\n"
                f"🔎 Main cost movement: {pressure}.\n\n"
                f"⚠️ Notable expense increases:\n"
                f"{cost_text}\n\n"
                f"📌 Largest current expense contributor: "
                f"{largest_expense_product} "
                f"(₹{largest_expense_value:,.2f})\n\n"
                f"💡 Business action: {action}"
            )

        except Exception:
            return (
                "I couldn't analyze expense performance because "
                "the available expense, revenue, product, or date "
                "data could not be processed."
            )

    # =========================================================
    # EXPENSE DIAGNOSIS
    # =========================================================

    expense_change_words = (
        "increase",
        "increased",
        "increasing",
        "rise",
        "risen",
        "rising",
        "grow",
        "growing",
        "grew",
        "change",
        "changed",
        "decrease",
        "decreased",
        "decline",
        "declined"
    )

    if (
        ("expense" in question or "expenses" in question)
        and (
            "why" in question
            or any(word in question for word in expense_change_words)
        )
        and "trend" not in question
    ):

        try:
            expense_df = df.copy()

            expense_df["date"] = pd.to_datetime(
                expense_df["date"]
            )

            daily_expense = (
                expense_df
                .groupby("date")
                .agg(
                    revenue=("revenue", "sum"),
                    expense=("expense", "sum"),
                    units=("quantity_sold", "sum")
                )
                .sort_index()
            )

            if len(daily_expense) < 2:
                return (
                    "I need data from at least two different dates "
                    "to analyze your expense trend."
                )

            # -------------------------------------------------
            # Compare first 7 days with latest 7 days
            # -------------------------------------------------

            window_size = min(7, len(daily_expense))

            first_period = daily_expense.iloc[:window_size]
            latest_period = daily_expense.iloc[-window_size:]

            first_expense = first_period["expense"].sum()
            latest_expense = latest_period["expense"].sum()

            first_revenue = first_period["revenue"].sum()
            latest_revenue = latest_period["revenue"].sum()

            first_units = first_period["units"].sum()
            latest_units = latest_period["units"].sum()

            expense_change = latest_expense - first_expense

            expense_change_pct = (
                (expense_change / first_expense) * 100
                if first_expense != 0
                else 0
            )

            # -------------------------------------------------
            # Expense-to-revenue ratio
            # -------------------------------------------------

            first_expense_ratio = (
                (first_expense / first_revenue) * 100
                if first_revenue > 0
                else 0
            )

            latest_expense_ratio = (
                (latest_expense / latest_revenue) * 100
                if latest_revenue > 0
                else 0
            )

            ratio_change = (
                latest_expense_ratio - first_expense_ratio
            )

            # -------------------------------------------------
            # Expense per unit
            # -------------------------------------------------

            first_expense_per_unit = (
                first_expense / first_units
                if first_units > 0
                else 0
            )

            latest_expense_per_unit = (
                latest_expense / latest_units
                if latest_units > 0
                else 0
            )

            expense_per_unit_change_pct = (
                (
                    (latest_expense_per_unit - first_expense_per_unit)
                    / first_expense_per_unit
                ) * 100
                if first_expense_per_unit > 0
                else 0
            )

            # -------------------------------------------------
            # Product-level expense contribution
            # -------------------------------------------------

            product_expense = (
                expense_df
                .groupby("product")["expense"]
                .sum()
                .sort_values(ascending=False)
            )

            highest_expense_product = (
                product_expense.index[0]
                if not product_expense.empty
                else "Unknown"
            )

            highest_expense_value = (
                product_expense.iloc[0]
                if not product_expense.empty
                else 0
            )

            # -------------------------------------------------
            # Determine likely reason
            # -------------------------------------------------

            if expense_per_unit_change_pct > 10:

                reason = (
                    "The increase appears to be mainly related to "
                    "higher expense per unit, suggesting that the "
                    "cost of products or operations may have increased."
                )

            elif ratio_change > 5:

                reason = (
                    "Expenses are growing faster relative to revenue, "
                    "which is putting additional pressure on profitability."
                )

            elif latest_units > first_units * 1.10:

                reason = (
                    "Higher sales volume may be contributing to the "
                    "increase in expenses because more units are being sold."
                )

            elif expense_change > 0:

                reason = (
                    "The expense increase appears to be a combination "
                    "of changes in sales volume, product mix, and operating costs."
                )

            else:

                reason = (
                    "Overall expenses have not increased significantly "
                    "between the comparison periods."
                )

            # -------------------------------------------------
            # Build response
            # -------------------------------------------------

            if expense_change > 0:

                return (
                    f"Your expenses increased by "
                    f"{expense_change_pct:.1f}% when comparing the "
                    f"first {window_size} days with the latest "
                    f"{window_size} days. "

                    f"Expenses changed from "
                    f"₹{first_expense:,.2f} to "
                    f"₹{latest_expense:,.2f}. "

                    f"The expense-to-revenue ratio changed from "
                    f"{first_expense_ratio:.1f}% to "
                    f"{latest_expense_ratio:.1f}%. "

                    f"Expense per unit changed by "
                    f"{expense_per_unit_change_pct:.1f}%. "

                    f"{reason} "

                    f"{highest_expense_product} currently contributes "
                    f"the highest total expense at "
                    f"₹{highest_expense_value:,.2f}. "

                    "Consider reviewing supplier prices, operating "
                    "costs, product-level expenses, and purchasing "
                    "quantities before the next business cycle."
                )

            elif expense_change < 0:

                return (
                    f"Your expenses decreased by "
                    f"{abs(expense_change_pct):.1f}% when comparing "
                    f"the first {window_size} days with the latest "
                    f"{window_size} days. "

                    f"Expenses changed from "
                    f"₹{first_expense:,.2f} to "
                    f"₹{latest_expense:,.2f}. "

                    f"The expense-to-revenue ratio changed from "
                    f"{first_expense_ratio:.1f}% to "
                    f"{latest_expense_ratio:.1f}%. "

                    "This suggests that your cost position has "
                    "improved over the comparison period. "
                    "Continue monitoring major expense categories "
                    "to maintain this improvement."
                )

            else:

                return (
                    f"Your expenses remained relatively stable when "
                    f"comparing the first {window_size} days with the "
                    f"latest {window_size} days. "

                    f"Expenses were approximately "
                    f"₹{latest_expense:,.2f}. "

                    f"The current expense-to-revenue ratio is "
                    f"{latest_expense_ratio:.1f}%. "
                    "Continue monitoring costs and major expense "
                    "contributors to protect your profit margin."
                )
        except Exception:
            return (
                "I couldn't analyze the expense trend because "
                "the expense or date data could not be processed."
            )
    # ---------------------------------------------------------
    # PRODUCT PERFORMING BADLY
    # ---------------------------------------------------------

    if (
        "why" in question
        and (
            "performing badly" in question
            or "performing poorly" in question
            or "not performing" in question
        )
    ):

        matched_product = None

        for product in product_data["product"]:
            if str(product).lower() in question:
                matched_product = product
                break

        if matched_product is None:
            return (
                "Please mention the product name so I can "
                "analyze its performance."
            )

        product_row = product_data[
            product_data["product"] == matched_product
        ].iloc[0]

        revenue = product_row["revenue"]
        expense = product_row["expense"]
        profit = product_row["profit"]
        units = product_row["quantity_sold"]

        margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        return (
            f"{matched_product} has relatively weak performance "
            f"with ₹{revenue:,.2f} in revenue, "
            f"{units:,.0f} units sold, and "
            f"₹{profit:,.2f} in profit. "
            f"Its product-level profit margin is {margin:.1f}%. "
            "Review its sales volume, pricing, demand, and "
            "expenses to identify opportunities for improvement."
        )

    # =========================================================
    # INVENTORY INTELLIGENCE
    # =========================================================

    if (
        (
            "inventory" in question
            or "stock" in question
            or "products" in question
            or "items" in question
        )
        and (
            "fast" in question
            or "slow" in question
            or "moving" in question
            or "sell" in question
            or "selling" in question
            or "velocity" in question
            or "demand" in question
            or "popular" in question
            or "top" in question
            or "best" in question
            or "attention" in question
        )
    ):

        try:
            inventory_df = df.copy()

            required_columns = [
                "product",
                "quantity_sold",
                "revenue",
                "date"
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in inventory_df.columns
            ]

            if missing_columns:
                return (
                    "I can't analyze product demand because the dataset "
                    "is missing: "
                    + ", ".join(missing_columns)
                    + "."
                )

            inventory_df["date"] = pd.to_datetime(
                inventory_df["date"]
            )

            product_summary = (
                inventory_df
                .groupby("product")
                .agg(
                    units_sold=("quantity_sold", "sum"),
                    revenue=("revenue", "sum"),
                    active_days=("date", "nunique")
                )
                .sort_values(
                    "units_sold",
                    ascending=False
                )
            )

            if product_summary.empty:
                return (
                    "I couldn't find enough product sales data "
                    "to analyze demand."
                )

            total_days = (
                inventory_df["date"].nunique()
            )

            product_summary["sales_velocity"] = (
                product_summary["units_sold"]
                / total_days
                if total_days > 0
                else 0
            )

            question_lower = question.lower()

            if (
                "slow" in question_lower
                or "slow-moving" in question_lower
                or "slow moving" in question_lower
            ):
                selected = (
                    product_summary
                    .sort_values("units_sold")
                    .head(5)
                )

                lines = []
                for product, row in selected.iterrows():
                    lines.append(
                        f"• {product}: "
                        f"{row['units_sold']:,.0f} units sold "
                        f"({row['sales_velocity']:.2f} units/day)"
                    )

                action = (
                    "Review slow-moving products before committing "
                    "additional purchasing budget. Their sales activity "
                    "should be compared with margin and current stock "
                    "before deciding whether to reorder."
                )

                heading = "🐌 Slow-moving products"

            else:
                selected = product_summary.head(5)

                lines = []
                for product, row in selected.iterrows():
                    lines.append(
                        f"• {product}: "
                        f"{row['units_sold']:,.0f} units sold "
                        f"({row['sales_velocity']:.2f} units/day)"
                    )

                action = (
                    "Prioritize availability of the fastest-moving "
                    "products and monitor their sales velocity regularly. "
                    "This is demand-based planning; actual stock levels "
                    "are not available in the current dataset."
                )

                heading = "🚀 Fast-moving products"

            return (
                f"📦 Inventory Intelligence\n\n"
                f"{heading}\n\n"
                f"{chr(10).join(lines)}\n\n"
                f"📅 Recorded sales period: "
                f"{inventory_df['date'].min().date()} to "
                f"{inventory_df['date'].max().date()}\n\n"
                f"💡 Business action: {action}"
            )

        except Exception:
            return (
                "I couldn't analyze product demand because the "
                "available product, sales, or date data could not "
                "be processed."
            )

    # =========================================================
    # PROFIT INTELLIGENCE
    # =========================================================

    if (
        "profit" in question
        and (
            "performing" in question
            or "performance" in question
            or "how is" in question
            or "trend" in question
            or "doing" in question
            or "happening" in question
            or "change" in question
        )
        and "why" not in question
    ):

        try:
            profit_df = df.copy()
            profit_df["date"] = pd.to_datetime(profit_df["date"])

            daily_data = (
                profit_df.groupby("date")
                .agg(revenue=("revenue", "sum"), expense=("expense", "sum"))
                .sort_index()
            )
            daily_data["profit"] = daily_data["revenue"] - daily_data["expense"]

            if len(daily_data) < 2:
                return "I need data from at least two different dates to analyze your profit performance."

            if len(daily_data) >= 14:
                first_period = profit_df[profit_df["date"].isin(daily_data.index[:7])]
                latest_period = profit_df[profit_df["date"].isin(daily_data.index[-7:])]
            else:
                midpoint = len(daily_data) // 2
                first_period = profit_df[profit_df["date"].isin(daily_data.index[:midpoint])]
                latest_period = profit_df[profit_df["date"].isin(daily_data.index[midpoint:])]

            first_revenue = first_period["revenue"].sum()
            latest_revenue = latest_period["revenue"].sum()
            first_expense = first_period["expense"].sum()
            latest_expense = latest_period["expense"].sum()
            first_profit = first_revenue - first_expense
            latest_profit = latest_revenue - latest_expense

            profit_change = latest_profit - first_profit
            profit_change_pct = (profit_change / abs(first_profit) * 100) if first_profit != 0 else 0
            first_margin = (first_profit / first_revenue * 100) if first_revenue > 0 else 0
            latest_margin = (latest_profit / latest_revenue * 100) if latest_revenue > 0 else 0
            margin_change = latest_margin - first_margin

            if profit_change > 2:
                direction = "increased"
            elif profit_change < -2:
                direction = "decreased"
            else:
                direction = "remained relatively stable"

            # Product-level profit comparison
            first_products = first_period.groupby("product").agg(
                revenue=("revenue", "sum"),
                expense=("expense", "sum")
            )
            latest_products = latest_period.groupby("product").agg(
                revenue=("revenue", "sum"),
                expense=("expense", "sum")
            )
            first_products["profit"] = first_products["revenue"] - first_products["expense"]
            latest_products["profit"] = latest_products["revenue"] - latest_products["expense"]

            products = sorted(set(first_products.index) | set(latest_products.index))
            product_rows = []
            for product in products:
                fp = first_products["profit"].get(product, 0)
                lp = latest_products["profit"].get(product, 0)
                product_rows.append({"product": product, "first_profit": fp, "latest_profit": lp, "profit_change": lp - fp})

            product_result = pd.DataFrame(product_rows)
            losers = product_result.sort_values("profit_change").head(2)
            gainers = product_result.sort_values("profit_change", ascending=False).head(2)

            if direction == "decreased":
                if latest_revenue < first_revenue and latest_expense > first_expense:
                    driver = "lower revenue combined with higher expenses"
                elif latest_revenue < first_revenue:
                    driver = "lower revenue"
                elif latest_expense > first_expense:
                    driver = "higher expenses"
                else:
                    driver = "changes in the revenue and expense mix"
                action = "Review the products driving the profit decline, pricing, and major cost increases before trying to increase sales volume."
            elif direction == "increased":
                if latest_revenue > first_revenue and latest_expense <= first_expense:
                    driver = "higher revenue with controlled expenses"
                elif latest_revenue > first_revenue:
                    driver = "higher revenue"
                elif latest_expense < first_expense:
                    driver = "lower expenses"
                else:
                    driver = "changes in the revenue and expense mix"
                action = "Protect the products and cost controls contributing to the improvement, and monitor whether the stronger margin continues."
            else:
                driver = "relatively stable revenue and expense performance"
                action = "Look for products with weak margins and opportunities to improve pricing or reduce unnecessary costs."

            loser_text = []
            for _, row in losers.iterrows():
                if row["profit_change"] < 0:
                    loser_text.append(f"{row['product']} (₹{abs(row['profit_change']):,.2f} lower profit)")
            gainer_text = []
            for _, row in gainers.iterrows():
                if row["profit_change"] > 0:
                    gainer_text.append(f"{row['product']} (₹{row['profit_change']:,.2f} higher profit)")

            product_insight = ""
            if loser_text:
                product_insight += "\n🔻 Biggest profit pressure: " + ", ".join(loser_text) + "."
            if gainer_text:
                product_insight += "\n🏆 Strongest profit contributors to the improvement: " + ", ".join(gainer_text) + "."

            return (
                f"💰 Profit Performance\n\n"
                f"Your profit {direction} by ₹{abs(profit_change):,.2f} "
                f"({abs(profit_change_pct):.1f}%) between the comparison periods.\n\n"
                f"First period profit: ₹{first_profit:,.2f}\n"
                f"Latest period profit: ₹{latest_profit:,.2f}\n"
                f"Profit margin: {first_margin:.1f}% → {latest_margin:.1f}% "
                f"({margin_change:+.1f} percentage points)\n\n"
                f"🔎 Main driver: {driver}."
                f"{product_insight}\n"
                f"💡 Business action: {action}"
            )

        except Exception:
            return "I couldn't analyze profit performance because the available revenue, expense, product, or date data could not be processed."

    # =========================================================
    # PROFIT CHANGE / TREND DIAGNOSIS
    # =========================================================

    if (
        "why" in question
        and "profit" in question
        and (
            "change" in question
            or "changed" in question
            or "decrease" in question
            or "decreased" in question
            or "increase" in question
            or "increased" in question
            or "trend" in question
        )
    ):

        try:

            trend_df = df.copy()

            trend_df["date"] = pd.to_datetime(
                trend_df["date"]
            )

            daily_data = (
                trend_df
                .groupby("date")
                .agg(
                    revenue=("revenue", "sum"),
                    expense=("expense", "sum")
                )
                .sort_index()
            )

            daily_data["profit"] = (
                daily_data["revenue"]
                - daily_data["expense"]
            )

            if len(daily_data) < 2:
                return (
                    "I need data from at least two different "
                    "dates to explain how your profit changed."
                )

            first_profit = daily_data["profit"].iloc[0]
            last_profit = daily_data["profit"].iloc[-1]

            profit_change = last_profit - first_profit

            first_revenue = daily_data["revenue"].iloc[0]
            last_revenue = daily_data["revenue"].iloc[-1]

            first_expense = daily_data["expense"].iloc[0]
            last_expense = daily_data["expense"].iloc[-1]

            revenue_change = last_revenue - first_revenue
            expense_change = last_expense - first_expense

            if profit_change > 0:

                if revenue_change > expense_change:

                    reason = (
                        "Revenue increased more than expenses, "
                        "which helped improve profit."
                    )

                else:

                    reason = (
                        "Profit increased based on the combined "
                        "change in revenue and expenses."
                    )

                return (
                    f"Your profit increased by "
                    f"₹{profit_change:,.2f} between "
                    f"{daily_data.index[0].date()} and "
                    f"{daily_data.index[-1].date()}. "
                    f"{reason} "
                    f"Revenue changed by ₹{revenue_change:,.2f}, "
                    f"while expenses changed by "
                    f"₹{expense_change:,.2f}."
                )

            elif profit_change < 0:

                return (
                    f"Your profit decreased by "
                    f"₹{abs(profit_change):,.2f} between "
                    f"{daily_data.index[0].date()} and "
                    f"{daily_data.index[-1].date()}. "
                    f"Revenue changed by ₹{revenue_change:,.2f}, "
                    f"while expenses changed by "
                    f"₹{expense_change:,.2f}. "
                    "These changes help explain the movement "
                    "in your profit."
                )

            else:

                return (
                    "Your profit remained unchanged between "
                    "the first and last recorded dates."
                )

        except Exception:

            return (
                "I couldn't analyze the profit trend because "
                "the date data could not be processed."
            )

    # =========================================================
    # REVENUE DECLINE DIAGNOSIS
    # =========================================================

    if (
        "revenue" in question
        and (
            "why" in question
            or "reason" in question
            or "cause" in question
            or "decreased" in question
            or "declined" in question
            or "drop" in question
        )
    ):

        try:

            analysis_df = df.copy()

            analysis_df["date"] = pd.to_datetime(
                analysis_df["date"]
            )

            analysis_df = analysis_df.sort_values("date")

            unique_dates = (
                analysis_df["date"]
                .drop_duplicates()
                .sort_values()
                .reset_index(drop=True)
            )

            if len(unique_dates) < 14:

                return (
                    "I need at least 14 unique dates to "
                    "diagnose a revenue decline reliably."
                )

            first_dates = unique_dates.iloc[:7]
            last_dates = unique_dates.iloc[-7:]

            first_period = analysis_df[
                analysis_df["date"].isin(first_dates)
            ]

            last_period = analysis_df[
                analysis_df["date"].isin(last_dates)
            ]

            first_revenue = first_period["revenue"].sum()
            last_revenue = last_period["revenue"].sum()

            first_units = first_period[
                "quantity_sold"
            ].sum()

            last_units = last_period[
                "quantity_sold"
            ].sum()

            revenue_change = (
                last_revenue - first_revenue
            )

            revenue_change_percent = (
                (revenue_change / first_revenue) * 100
                if first_revenue != 0
                else 0
            )

            units_change_percent = (
                (
                    (last_units - first_units)
                    / first_units
                ) * 100
                if first_units != 0
                else 0
            )

            first_revenue_per_unit = (
                first_revenue / first_units
                if first_units != 0
                else 0
            )

            last_revenue_per_unit = (
                last_revenue / last_units
                if last_units != 0
                else 0
            )

            revenue_per_unit_change_percent = (
                (
                    (
                        last_revenue_per_unit
                        - first_revenue_per_unit
                    )
                    / first_revenue_per_unit
                ) * 100
                if first_revenue_per_unit != 0
                else 0
            )

            # -------------------------------------------------
            # PRODUCT MIX
            # -------------------------------------------------

            first_product_revenue = (
                first_period
                .groupby("product")["revenue"]
                .sum()
            )

            last_product_revenue = (
                last_period
                .groupby("product")["revenue"]
                .sum()
            )

            all_products = sorted(
                set(first_product_revenue.index)
                | set(last_product_revenue.index)
            )

            mix_data = []

            for product in all_products:

                first_product_value = (
                    first_product_revenue.get(
                        product,
                        0
                    )
                )

                last_product_value = (
                    last_product_revenue.get(
                        product,
                        0
                    )
                )

                first_share = (
                    first_product_value
                    / first_revenue
                    * 100
                    if first_revenue != 0
                    else 0
                )

                last_share = (
                    last_product_value
                    / last_revenue
                    * 100
                    if last_revenue != 0
                    else 0
                )

                share_change = (
                    last_share - first_share
                )

                mix_data.append({
                    "product": product,
                    "first_share": first_share,
                    "last_share": last_share,
                    "share_change": share_change
                })

            mix_result = pd.DataFrame(mix_data)

            declining_mix = mix_result[
                mix_result["share_change"] < 0
            ]

            growing_mix = mix_result[
                mix_result["share_change"] > 0
            ]

            # -------------------------------------------------
            # DETERMINE MAIN REASON
            # -------------------------------------------------

            if (
                revenue_per_unit_change_percent < 0
                and abs(
                    revenue_per_unit_change_percent
                ) > abs(units_change_percent)
            ):

                reason = (
                    "a lower average revenue per unit"
                )

                explanation = (
                    "The product mix may have shifted toward "
                    "lower-value products."
                )

            elif units_change_percent < 0:

                reason = (
                    "lower sales volume"
                )

                explanation = (
                    "Fewer units were sold during the "
                    "latest comparison period."
                )

            else:

                reason = (
                    "a combination of sales volume and "
                    "revenue per unit changes"
                )

                explanation = (
                    "Both sales volume and the value generated "
                    "per unit contributed to the change."
                )

            # -------------------------------------------------
            # PRODUCT SHARE CHANGE
            # -------------------------------------------------

            mix_sentence = ""

            if not declining_mix.empty:

                biggest_loser = declining_mix.loc[
                    declining_mix["share_change"].idxmin()
                ]

                mix_sentence += (
                    f"{biggest_loser['product']} lost "
                    f"approximately "
                    f"{abs(biggest_loser['share_change']):.1f} "
                    f"percentage points of total revenue share"
                )

            if not growing_mix.empty:

                biggest_gainer = growing_mix.loc[
                    growing_mix["share_change"].idxmax()
                ]

                if mix_sentence:

                    mix_sentence += (
                        f", while "
                        f"{biggest_gainer['product']} gained "
                        f"approximately "
                        f"{biggest_gainer['share_change']:.1f} "
                        f"percentage points."
                    )

                else:

                    mix_sentence += (
                        f"{biggest_gainer['product']} gained "
                        f"approximately "
                        f"{biggest_gainer['share_change']:.1f} "
                        f"percentage points of total revenue share."
                    )

            return (
                f"Revenue decreased by "
                f"{abs(revenue_change_percent):.1f}% "
                f"when comparing the first 7 days with "
                f"the latest 7 days. "
                f"The decline appears to be mainly driven by "
                f"{reason}. "
                f"{explanation} "
                f"Sales volume changed by "
                f"{units_change_percent:.1f}%, while average "
                f"revenue per unit changed by "
                f"{revenue_per_unit_change_percent:.1f}%. "
                f"{mix_sentence} "
                "This suggests a shift in the product mix. "
                "Consider checking whether customers are "
                "buying lower-value products, whether pricing "
                "or discounts changed, and whether high-value "
                "products experienced weaker demand."
            )

        except Exception:

            return (
                "I couldn't diagnose the revenue decline because "
                "the available business data could not be processed."
            )

    # =========================================================
    # REVENUE PERFORMANCE ANALYSIS
    # =========================================================

    if (
        "revenue" in question
        and (
            "why" in question
            or "trend" in question
            or "change" in question
            or "changed" in question
            or "increase" in question
            or "increased" in question
            or "decrease" in question
            or "decreased" in question
            or "decline" in question
            or "declined" in question
            or "growth" in question
            or "growing" in question
            or "performing" in question
            or "performance" in question
            or "doing" in question
            or "happening" in question
            or "how is" in question
        )
        and not (
            "gained share" in question
            or "lost share" in question
            or "product mix" in question
        )
    ):

        try:
            revenue_df = df.copy()
            revenue_df["date"] = pd.to_datetime(revenue_df["date"])

            daily_data = (
                revenue_df
                .groupby("date")
                .agg(
                    revenue=("revenue", "sum"),
                    units=("quantity_sold", "sum")
                )
                .sort_index()
            )

            if len(daily_data) < 2:
                return (
                    "I need data from at least two different dates "
                    "to analyze your revenue performance."
                )

            average_daily_revenue = daily_data["revenue"].mean()
            first_date = daily_data.index[0]
            last_date = daily_data.index[-1]

            if len(daily_data) >= 14:
                first_period = daily_data.iloc[:7]
                latest_period = daily_data.iloc[-7:]
                period_label = "first 7 days vs latest 7 days"
            else:
                midpoint = len(daily_data) // 2
                if midpoint == 0:
                    return "I need data from at least two different dates to analyze revenue performance."
                first_period = daily_data.iloc[:midpoint]
                latest_period = daily_data.iloc[midpoint:]
                period_label = "first half vs second half of the recorded period"

            first_period_revenue = first_period["revenue"].sum()
            latest_period_revenue = latest_period["revenue"].sum()
            first_period_units = first_period["units"].sum()
            latest_period_units = latest_period["units"].sum()

            revenue_period_change = latest_period_revenue - first_period_revenue
            units_change = latest_period_units - first_period_units

            revenue_change_percent = (
                (revenue_period_change / first_period_revenue) * 100
                if first_period_revenue != 0 else 0
            )
            units_change_percent = (
                (units_change / first_period_units) * 100
                if first_period_units != 0 else 0
            )

            first_revenue_per_unit = (
                first_period_revenue / first_period_units
                if first_period_units > 0 else 0
            )
            latest_revenue_per_unit = (
                latest_period_revenue / latest_period_units
                if latest_period_units > 0 else 0
            )
            revenue_per_unit_change_percent = (
                (
                    (latest_revenue_per_unit - first_revenue_per_unit)
                    / first_revenue_per_unit
                ) * 100
                if first_revenue_per_unit != 0 else 0
            )

            if revenue_change_percent > 2:
                direction = "increased"
            elif revenue_change_percent < -2:
                direction = "decreased"
            else:
                direction = "remained relatively stable"

            if direction == "increased":
                if units_change_percent > 0 and revenue_per_unit_change_percent > 0:
                    driver = "both higher sales volume and higher revenue per unit"
                elif units_change_percent > 0:
                    driver = "higher sales volume"
                elif revenue_per_unit_change_percent > 0:
                    driver = "higher revenue per unit"
                else:
                    driver = "a combination of sales volume and revenue changes"
            elif direction == "decreased":
                if units_change_percent < 0 and revenue_per_unit_change_percent < 0:
                    driver = "both lower sales volume and lower revenue per unit"
                elif units_change_percent < 0:
                    driver = "lower sales volume"
                elif revenue_per_unit_change_percent < 0:
                    driver = "lower revenue per unit"
                else:
                    driver = "a combination of sales volume and revenue-per-unit changes"
            else:
                driver = "relatively stable sales volume and revenue per unit"

            # -------------------------------------------------
            # PRODUCT-LEVEL DRILLDOWN
            # -------------------------------------------------
            product_insight = ""
            product_action = ""

            required_columns = {"product", "revenue", "quantity_sold"}
            if required_columns.issubset(revenue_df.columns):
                first_product = (
                    revenue_df[revenue_df["date"].isin(first_period.index)]
                    .groupby("product")
                    .agg(revenue=("revenue", "sum"), units=("quantity_sold", "sum"))
                )
                latest_product = (
                    revenue_df[revenue_df["date"].isin(latest_period.index)]
                    .groupby("product")
                    .agg(revenue=("revenue", "sum"), units=("quantity_sold", "sum"))
                )

                all_products = sorted(set(first_product.index) | set(latest_product.index), key=str)
                product_rows = []

                for product in all_products:
                    first_rev = float(first_product["revenue"].get(product, 0))
                    latest_rev = float(latest_product["revenue"].get(product, 0))
                    first_units = float(first_product["units"].get(product, 0))
                    latest_units = float(latest_product["units"].get(product, 0))

                    first_rpu = first_rev / first_units if first_units > 0 else 0
                    latest_rpu = latest_rev / latest_units if latest_units > 0 else 0
                    rpu_change_pct = (
                        ((latest_rpu - first_rpu) / first_rpu) * 100
                        if first_rpu != 0 else 0
                    )
                    first_share = (
                        (first_rev / first_period_revenue) * 100
                        if first_period_revenue != 0 else 0
                    )
                    latest_share = (
                        (latest_rev / latest_period_revenue) * 100
                        if latest_period_revenue != 0 else 0
                    )

                    product_rows.append({
                        "product": product,
                        "revenue_change": latest_rev - first_rev,
                        "units_change": latest_units - first_units,
                        "rpu_change_pct": rpu_change_pct,
                        "share_change": latest_share - first_share,
                    })

                product_result = pd.DataFrame(product_rows)

                if not product_result.empty:
                    declining = product_result.sort_values("revenue_change").head(2)
                    growing = product_result.sort_values("revenue_change", ascending=False).head(2)

                    negative_rows = declining[declining["revenue_change"] < 0]
                    positive_rows = growing[growing["revenue_change"] > 0]

                    if direction == "decreased" and not negative_rows.empty:
                        insights = []
                        for _, row in negative_rows.iterrows():
                            text = (
                                f"{row['product']} had the largest revenue decline of "
                                f"₹{abs(row['revenue_change']):,.2f}"
                            )
                            if row["rpu_change_pct"] < -2:
                                text += f" and its revenue per unit fell {abs(row['rpu_change_pct']):.1f}%"
                            elif row["units_change"] < 0:
                                text += f" with units sold down by {abs(row['units_change']):,.0f}"
                            insights.append(text + ".")
                        product_insight = "🔎 Product-level insight\n" + "\n".join(insights)

                        if units_change_percent > 0 and revenue_per_unit_change_percent < 0:
                            product_action = (
                                "💡 Business action: Sales volume is already increasing. "
                                "Review the products above for pricing, discounting, and "
                                "lower-value mix changes rather than simply trying to sell more units."
                            )
                        else:
                            product_action = (
                                "💡 Business action: Review demand, pricing, and costs for "
                                "the products showing the largest revenue declines."
                            )

                    elif direction == "increased" and not positive_rows.empty:
                        insights = []
                        for _, row in positive_rows.iterrows():
                            insights.append(
                                f"{row['product']} added ₹{row['revenue_change']:,.2f} in revenue."
                            )
                        product_insight = "🔎 Product-level growth\n" + "\n".join(insights)
                        product_action = (
                            "💡 Business action: Protect the products driving growth and "
                            "check whether their demand can be scaled without weakening margins."
                        )
                    elif direction == "remained relatively stable":
                        product_insight = (
                            "🔎 Product-level insight\n"
                            "No major product-level revenue movement is strong enough to "
                            "explain a large overall change."
                        )

            if direction == "decreased":
                if units_change_percent > 0 and revenue_per_unit_change_percent < 0:
                    recommendation = (
                        "Sales volume is already increasing, but revenue per unit is falling. "
                        "Investigate discounts, price reductions, and shifts toward lower-value "
                        "products. Focus on improving product mix and revenue per sale rather "
                        "than simply increasing unit volume."
                    )
                elif units_change_percent < 0 and revenue_per_unit_change_percent < 0:
                    recommendation = (
                        "Both sales volume and revenue per unit are falling. Review demand, "
                        "pricing, discounts, and the performance of your main products."
                    )
                elif units_change_percent < 0:
                    recommendation = (
                        "Revenue is falling mainly because fewer units are being sold. "
                        "Investigate demand, customer activity, and the products losing volume."
                    )
                else:
                    recommendation = (
                        "Revenue is falling. Review product-level revenue, pricing, and sales "
                        "mix to identify the strongest source of pressure."
                    )
            elif direction == "increased":
                recommendation = (
                    "Revenue is improving. Continue monitoring the products and sales patterns "
                    "driving growth while protecting profitability."
                )
            else:
                recommendation = (
                    "Revenue is relatively stable. Look for opportunities to increase sales "
                    "volume or improve revenue per sale without weakening margins."
                )

            report = (
                f"📊 Revenue Performance\n\n"
                f"Your revenue {direction} by {abs(revenue_change_percent):.1f}% "
                f"when comparing the {period_label}.\n\n"
                f"💰 First period revenue: ₹{first_period_revenue:,.2f}\n"
                f"💰 Latest period revenue: ₹{latest_period_revenue:,.2f}\n"
                f"📦 Sales volume change: {units_change_percent:+.1f}%\n"
                f"💵 Revenue per unit change: {revenue_per_unit_change_percent:+.1f}%\n\n"
                f"🔎 Main driver: {driver}.\n\n"
                f"📈 Overall recorded period: {first_date.date()} to {last_date.date()}\n"
                f"Average daily revenue: ₹{average_daily_revenue:,.2f}\n\n"
                f"💡 Recommendation: {recommendation}"
            )

            if product_insight:
                report += f"\n\n{product_insight}"
            if product_action:
                report += f"\n\n{product_action}"

            return report

        except Exception:
            return (
                "I couldn't analyze the revenue performance because the available "
                "revenue, date, product, or sales-volume data could not be processed."
            )

    # =========================================================
    # PRODUCT MIX ANALYSIS
    # =========================================================

    if (
        "product mix" in question
        or "product mixture" in question
        or (
            "products" in question
            and (
                "gained share" in question
                or "lost share" in question
                or "changed" in question
            )
        )
    ):

        try:

            mix_df = df.copy()

            mix_df["date"] = pd.to_datetime(
                mix_df["date"]
            )

            unique_dates = (
                mix_df["date"]
                .drop_duplicates()
                .sort_values()
                .reset_index(drop=True)
            )

            if len(unique_dates) < 14:

                return (
                    "I need at least 14 unique dates to compare "
                    "the first 7 days with the latest 7 days "
                    "for product mix analysis."
                )

            first_dates = unique_dates.iloc[:7]
            last_dates = unique_dates.iloc[-7:]

            first_period = mix_df[
                mix_df["date"].isin(first_dates)
            ]

            last_period = mix_df[
                mix_df["date"].isin(last_dates)
            ]

            first_product_revenue = (
                first_period
                .groupby("product")["revenue"]
                .sum()
            )

            last_product_revenue = (
                last_period
                .groupby("product")["revenue"]
                .sum()
            )

            first_total = first_product_revenue.sum()
            last_total = last_product_revenue.sum()

            if first_total == 0 or last_total == 0:
                return (
                    "There is not enough revenue data to "
                    "analyze the product mix."
                )

            all_products = sorted(
                set(first_product_revenue.index)
                | set(last_product_revenue.index)
            )

            mix_data = []

            for product in all_products:

                first_revenue = first_product_revenue.get(
                    product,
                    0
                )

                last_revenue = last_product_revenue.get(
                    product,
                    0
                )

                first_share = (
                    first_revenue / first_total
                ) * 100

                last_share = (
                    last_revenue / last_total
                ) * 100

                share_change = (
                    last_share - first_share
                )

                mix_data.append({
                    "product": product,
                    "first_share": first_share,
                    "last_share": last_share,
                    "share_change": share_change
                })

            mix_result = pd.DataFrame(mix_data)

            biggest_loser = mix_result.loc[
                mix_result["share_change"].idxmin()
            ]

            biggest_gainer = mix_result.loc[
                mix_result["share_change"].idxmax()
            ]

            if biggest_loser["share_change"] < 0:

                loser_text = (
                    f"{biggest_loser['product']} decreased "
                    f"from {biggest_loser['first_share']:.1f}% "
                    f"to {biggest_loser['last_share']:.1f}% "
                    f"of total revenue."
                )

            else:

                loser_text = (
                    "No product lost meaningful revenue share "
                    "during the comparison period."
                )

            if biggest_gainer["share_change"] > 0:

                gainer_text = (
                    f"{biggest_gainer['product']} increased "
                    f"from {biggest_gainer['first_share']:.1f}% "
                    f"to {biggest_gainer['last_share']:.1f}% "
                    f"of total revenue."
                )

            else:

                gainer_text = (
                    "No product gained meaningful revenue share "
                    "during the comparison period."
                )

            return (
                f"{loser_text} "
                f"{gainer_text} "
                "Overall, the revenue mix shifted between "
                "the two comparison periods."
            )

        except Exception:

            return (
                "I couldn't analyze the product mix because "
                "the available date or product data could "
                "not be processed."
            )

    # =========================================================
    # PROFIT MARGIN DIAGNOSIS
    # =========================================================

    if (
        "why" in question
        and "profit margin" in question
    ):

        return (
            f"Your profit margin is {profit_margin:.1f}%. "
            "Profit margin shows how much of your revenue "
            "remains as profit after expenses. A higher margin "
            "generally means the business is keeping more of "
            "each rupee earned after covering its costs."
        )

    # =========================================================
    # EXPENSE DIAGNOSIS
    # =========================================================

    if (
        "why" in question
        and (
            "expense" in question
            or "expenses" in question
        )
    ):

        expense_ratio = (
            (total_expenses / total_revenue) * 100
            if total_revenue > 0
            else 0
        )

        highest_expense_index = (
            product_data["expense"].idxmax()
        )

        highest_expense_product = product_data.loc[
            highest_expense_index,
            "product"
        ]

        highest_expense = product_data.loc[
            highest_expense_index,
            "expense"
        ]

        return (
            f"Your expenses are ₹{total_expenses:,.2f}, "
            f"which is {expense_ratio:.1f}% of your revenue. "
            f"{highest_expense_product} has the highest expense "
            f"among your products at ₹{highest_expense:,.2f}. "
            "Reviewing the costs associated with this product "
            "could help improve your overall profit margin."
        )

    # =========================================================
    # FORECAST QUESTIONS
    # =========================================================

    if (
        "forecast" in question
        or "predict" in question
    ):

        if forecast_data is None:

            return (
                "Revenue forecast data is not available yet."
            )

        predicted_total = forecast_data[
            "predicted_revenue"
        ].sum()

        return (
            f"Based on the current forecast, BizPilot estimates "
            f"approximately ₹{predicted_total:,.2f} in revenue "
            f"over the forecast period."
        )

    # =========================================================
    # BUSINESS SUMMARY
    # =========================================================

    if (
        "summary" in question
        or "overall" in question
        or "business doing" in question
    ):

        top_revenue_index = (
            product_data["revenue"].idxmax()
        )

        top_profit_index = (
            product_data["profit"].idxmax()
        )

        top_revenue_product = product_data.loc[
            top_revenue_index,
            "product"
        ]

        top_profit_product = product_data.loc[
            top_profit_index,
            "product"
        ]

        return (
            f"Your business generated "
            f"₹{total_revenue:,.2f} in revenue and "
            f"₹{total_profit:,.2f} profit, "
            f"with a {profit_margin:.1f}% profit margin. "
            f"{top_revenue_product} is your highest-revenue "
            f"product, while {top_profit_product} generates "
            f"the highest profit."
        )

    # =========================================================
    # ACTION PLAN QUESTIONS
    # =========================================================

    if (
        "what should i do" in question
        or "what should i focus" in question
        or "what can i do" in question
        or "how can i increase profit" in question
        or "how can i improve profit" in question
        or "what should i improve" in question
    ):

        if recommendations:

            action_text = (
                "Based on your current business data, "
                "here are the main actions to consider:\n\n"
            )

            for i, recommendation in enumerate(
                recommendations[:3],
                start=1
            ):

                action_text += (
                    f"{i}. {recommendation}\n"
                )

            return action_text

        return (
            "I need more business performance data before "
            "I can generate an action plan."
        )

    # =========================================================
    # BASIC BUSINESS METRICS
    # =========================================================

    if (
        "profit margin" in question
        or "margin" in question
    ):

        return (
            f"Your current profit margin is "
            f"{profit_margin:.1f}%."
        )

    if (
        "expense" in question
        or "expenses" in question
    ):

        expense_ratio = (
            (total_expenses / total_revenue) * 100
            if total_revenue > 0
            else 0
        )

        return (
            f"Your total expenses are "
            f"₹{total_expenses:,.2f}, "
            f"which is {expense_ratio:.1f}% "
            f"of your revenue."
        )

    # IMPORTANT:
    # Only answer a simple revenue question here.
    # Diagnosis/trend questions are handled above.
    if (
    "revenue" in question
    and not (
        "why" in question
        or "reason" in question
        or "cause" in question
        or "decrease" in question
        or "decreased" in question
        or "decline" in question
        or "declined" in question
        or "drop" in question
        or "change" in question
        or "changed" in question
        or "increase" in question
        or "increased" in question
        or "trend" in question
        or "growth" in question
        or "growing" in question
        or "performing" in question
        or "performance" in question
        or "doing" in question
        or "happening" in question
        or "performing" in question
        or "performance" in question
        or "doing" in question
        or "how is" in question
        or "happening" in question
        or "product mix" in question
        or "gained share" in question
        or "lost share" in question
    )
):
        return (
        f"Your total revenue is "
        f"₹{total_revenue:,.2f}."
    )
    if "profit" in question:

        return (
            f"Your total profit is "
            f"₹{total_profit:,.2f}."
        )

    # =========================================================
    # DEFAULT RESPONSE
    # =========================================================

    return (
        "I can help you analyze your business data. "
        "You can ask about revenue, revenue trends, "
        "revenue decline, product mix, expenses, profit, "
        "profit margin, best-selling products, highest-profit "
        "products, lowest-revenue products, forecasts, "
        "or your overall business summary."
    )