import os
import pandas as pd
import sqlite3

def test_output_files():
    # Check if the output files exist
    assert os.path.isfile("../data/carbon_dioxide.db"), "carbon_dioxide.db does not exist."
    assert os.path.isfile("../data/surface_temperature.db"), "surface_temperature.db does not exist."

    # Check the content of the carbon dioxide database
    with sqlite3.connect("../data/carbon_dioxide.db") as conn:
        df_carbon = pd.read_sql_query("SELECT * FROM carbon_dioxide", conn)
        assert not df_carbon.empty, "carbon_dioxide table is empty."

        # Check schema
        expected_columns = {'ObjectId', 'Country', 'Unit', 'Date', 'Value'}
        assert set(df_carbon.columns) == expected_columns, f"Unexpected columns in carbon_dioxide table: {df_carbon.columns}"
        # Validate data types
        assert pd.api.types.is_numeric_dtype(df_carbon['Value']), "'Value' column should be numeric"
        

    # Check the content of the surface temperature database
    with sqlite3.connect("../data/surface_temperature.db") as conn:
        df_temp = pd.read_sql_query("SELECT * FROM surface_temperature", conn)
        assert not df_temp.empty, "surface_temperature table is empty."
        # Check schema
        expected_columns = {'ObjectId', 'Country', 'Unit'} | {f'F{year}' for year in range(1961, 2024)}
        assert set(df_temp.columns) == expected_columns, f"Unexpected columns in surface_temperature table: {df_temp.columns}"


if __name__ == "__main__":
    test_output_files()
    print("All tests passed.")
