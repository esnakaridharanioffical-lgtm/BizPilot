import pandas as pd


def load_business_data(uploaded_file):
    """
    Load business data from a CSV or Excel file.
    """

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format. Please upload CSV or Excel.")

    return df


def clean_business_data(df):
    """
    Basic cleaning of uploaded business data.
    """

    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df