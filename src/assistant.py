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
    # REVENUE TREND DIAGNOSIS
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
        )
        and not (
            "gained share" in question
            or "lost share" in question
            or "product mix" in question
        )
    ):

        try:

            revenue_df = df.copy()

            revenue_df["date"] = pd.to_datetime(
                revenue_df["date"]
            )

            daily_revenue = (
                revenue_df
                .groupby("date")["revenue"]
                .sum()
                .sort_index()
            )

            if len(daily_revenue) < 2:
                return (
                    "I need data from at least two different "
                    "dates to analyze your revenue trend."
                )

            first_revenue = daily_revenue.iloc[0]
            last_revenue = daily_revenue.iloc[-1]

            revenue_change = last_revenue - first_revenue

            if first_revenue != 0:
                change_percent = (
                    revenue_change / first_revenue
                ) * 100
            else:
                change_percent = 0

            average_daily_revenue = daily_revenue.mean()

            if revenue_change > 0:

                direction = "increased"
                absolute_change = revenue_change

            elif revenue_change < 0:

                direction = "decreased"
                absolute_change = abs(revenue_change)

            else:

                return (
                    f"Your revenue remained stable between "
                    f"{daily_revenue.index[0].date()} and "
                    f"{daily_revenue.index[-1].date()}. "
                    f"Your average daily revenue was "
                    f"₹{average_daily_revenue:,.2f}."
                )

            return (
                f"Your revenue {direction} from "
                f"₹{first_revenue:,.2f} to "
                f"₹{last_revenue:,.2f} between "
                f"{daily_revenue.index[0].date()} and "
                f"{daily_revenue.index[-1].date()}. "
                f"That is a {direction} of "
                f"₹{absolute_change:,.2f} "
                f"({abs(change_percent):.1f}%). "
                f"Your average daily revenue during this "
                f"period was ₹{average_daily_revenue:,.2f}."
            )

        except Exception:

            return (
                "I couldn't analyze the revenue trend because "
                "the date data could not be processed."
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