"""
Aplica tipos de dados a um DataFrame.
"""
import pandas as pd


def aplicar_tipos_colunas(df, dicionario_tipos):
    """
    Apply data types to a DataFrame based on a dictionary, using pd.to_numeric
    for numeric types with coercion when necessary.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        type_dict (dict): A dictionary mapping column names to desired data types.

    Returns:
        pd.DataFrame: The DataFrame with updated column types.
    """
    for col, dtype in dicionario_tipos.items():
        if col in df.columns:
            try:
                if dtype == "datetime64[ns]":
                    # Convert to datetime, coercing invalid entries to NaT
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                elif dtype == "float64" or dtype == "np.Int64":
                    # Convert to numeric, coercing invalid entries to NaN
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    # For Int64, convert from float to nullable integer type
                    if dtype == "Int64":
                        df[col] = df[col].astype("Int64")
                else:
                    # Apply general type conversion
                    df[col] = df[col].astype(dtype)
            except Exception as e:
                print(f"Error converting column {col} to {dtype}: {e}")
        else:
            print(f"Column {col} not found in DataFrame.")
    return df
