import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


def forecast_revenue(df, days=7):
    """
    Forecast future daily revenue using historical revenue patterns.
    """

    data = df.copy()

    # Prepare dates
    data["date"] = pd.to_datetime(data["date"])

    # Aggregate revenue by day
    daily = (
        data.groupby("date", as_index=False)["revenue"]
        .sum()
        .sort_values("date")
    )

    # Create time-based features
    daily["day_of_week"] = daily["date"].dt.dayofweek
    daily["lag_1"] = daily["revenue"].shift(1)
    daily["lag_7"] = daily["revenue"].shift(7)
    daily["rolling_7"] = (
        daily["revenue"].shift(1).rolling(7).mean()
    )

    # Remove rows without enough history
    training_data = daily.dropna().copy()

    features = [
        "day_of_week",
        "lag_1",
        "lag_7",
        "rolling_7"
    ]

    # Train Random Forest model
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=8
    )

    model.fit(
        training_data[features],
        training_data["revenue"]
    )

    # Store historical revenue for recursive forecasting
    history = daily[["date", "revenue"]].copy()

    predictions = []

    for _ in range(days):

        next_date = history["date"].max() + pd.Timedelta(days=1)

        lag_1 = history["revenue"].iloc[-1]

        if len(history) >= 7:
            lag_7 = history["revenue"].iloc[-7]
            rolling_7 = history["revenue"].iloc[-7:].mean()
        else:
            lag_7 = lag_1
            rolling_7 = history["revenue"].mean()

        input_data = pd.DataFrame({
            "day_of_week": [next_date.dayofweek],
            "lag_1": [lag_1],
            "lag_7": [lag_7],
            "rolling_7": [rolling_7]
        })

        prediction = model.predict(input_data)[0]

        prediction = max(0, prediction)

        predictions.append({
            "date": next_date,
            "predicted_revenue": prediction
        })

        history = pd.concat(
            [
                history,
                pd.DataFrame({
                    "date": [next_date],
                    "revenue": [prediction]
                })
            ],
            ignore_index=True
        )

    return pd.DataFrame(predictions)


def evaluate_forecast_model(df):
    """
    Evaluate the forecasting model using Mean Absolute Error (MAE).
    """

    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])

    daily = (
        data.groupby("date", as_index=False)["revenue"]
        .sum()
        .sort_values("date")
    )

    daily["day_of_week"] = daily["date"].dt.dayofweek
    daily["lag_1"] = daily["revenue"].shift(1)
    daily["lag_7"] = daily["revenue"].shift(7)
    daily["rolling_7"] = (
        daily["revenue"].shift(1).rolling(7).mean()
    )

    daily = daily.dropna().copy()

    features = [
        "day_of_week",
        "lag_1",
        "lag_7",
        "rolling_7"
    ]

    # Use the first 80% for training
    split_index = int(len(daily) * 0.8)

    train = daily.iloc[:split_index]
    test = daily.iloc[split_index:]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=8
    )

    model.fit(
        train[features],
        train["revenue"]
    )

    predictions = model.predict(test[features])

    mae = mean_absolute_error(
        test["revenue"],
        predictions
    )

    return mae