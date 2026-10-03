def generate_recommendations(
    total_revenue,
    total_expenses,
    total_profit,
    product_data,
    profit_margin
):
    """
    Generate actionable business recommendations
    based on business performance.
    """

    recommendations = []

    # Profit analysis
    if profit_margin < 10:
        recommendations.append(
            "⚠️ Profit margin is very low. Review expenses and pricing."
        )
    elif profit_margin < 20:
        recommendations.append(
            "📊 Profit margin could be improved. Consider reducing unnecessary costs."
        )
    else:
        recommendations.append(
            "✅ Profit margin is healthy. Focus on maintaining consistent performance."
        )

    # Expense analysis
    expense_ratio = (
        total_expenses / total_revenue
    ) * 100 if total_revenue > 0 else 0

    if expense_ratio > 70:
        recommendations.append(
            "💸 Expenses are consuming a large portion of revenue. "
            "Look for areas where operating costs can be reduced."
        )

    # Product analysis
    top_profit_product = product_data.loc[
        product_data["profit"].idxmax(),
        "product"
    ]

    lowest_revenue_product = product_data.loc[
        product_data["revenue"].idxmin(),
        "product"
    ]

    recommendations.append(
        f"🏆 {top_profit_product} is your highest-profit product. "
        "Consider maintaining inventory and promoting it."
    )

    recommendations.append(
        f"📉 {lowest_revenue_product} has the lowest revenue. "
        "Review its pricing, demand, and marketing performance."
    )

    # General growth recommendation
    if total_profit > 0:
        recommendations.append(
            "🚀 The business is generating positive profit. "
            "Use the highest-performing products as a foundation for growth."
        )
    else:
        recommendations.append(
            "⚠️ The business is currently operating at a loss. "
            "Focus on improving revenue and controlling expenses."
        )

    return recommendations