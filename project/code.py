import requests
import geojson
import csv
import pandas as pd
import os
import sqlite3


def fetch_geojson_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return geojson.loads(response.text)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def geojson_to_csv(geojson_data, csv_filename):
    if geojson_data:
        features = geojson_data.get('features', [])
        
        # Assuming all features have the same structure
        if features:
            # Extract the field names from the first feature's properties
            fieldnames = features[0]['properties'].keys()
            # Open the CSV file for writing
            with open(csv_filename, mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for feature in features:
                    writer.writerow(feature['properties'])
            print(f"Data successfully written to {csv_filename}")
        else:
            print("No features found in GeoJSON data.")
    else:
        print("No GeoJSON data to process.")

def save_to_sqlite(df, db_path, table_name):
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully written to {db_path} in table {table_name}")

if __name__ == "__main__":
    url = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Indicator_3_2_Climate_Indicators_Monthly_Atmospheric_Carbon_Dioxide_concentrations/FeatureServer/0/query?where=1=1&outFields=*&f=geojson"
    geojson_data = fetch_geojson_data(url)
    if geojson_data:
        csv_filename = os.path.join("..", "data", "carbon_dioxide.csv")
        
        geojson_to_csv(geojson_data, csv_filename)

    df = pd.read_csv(csv_filename)

    # Drop the 'ISO2', 'ISO3', etc. (not needed columns) if they exist
    df = df.drop(columns=['ISO2', 'ISO3', 'Indicator', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor'], errors='ignore')
          
    # Ensure the 'Value' column is numeric 
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # Drop rows with invalid 'Date' or 'Value'
    df = df.dropna(subset=['Date', 'Value'])

    db_path = os.path.join("..", "data", "carbon_dioxide.db")
    save_to_sqlite(df, db_path, "carbon_dioxide")

    # Delete the CSV file after saving to the database
    os.remove(csv_filename)
    
    url = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature/FeatureServer/0/query?where=1=1&outFields=*&f=geojson"
    geojson_data = fetch_geojson_data(url)
    if geojson_data:
        csv_filename = os.path.join("..","data", "surface_temperature.csv")
        
        geojson_to_csv(geojson_data, csv_filename)

    df = pd.read_csv(csv_filename)
    
    # Drop the 'ISO2', 'ISO3', etc. (not needed columns) if they exist
    df = df.drop(columns=['ISO2', 'ISO3', 'Indicator', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor'], errors='ignore')
    
    # Check if values in columns from 'F1961' to 'F2023' are decimal numbers
    cols_to_check = df.loc[:, 'F1961':'F2023']
    is_decimal = cols_to_check.apply(lambda col: col.map(lambda x: isinstance(x, float) or (isinstance(x, str) and x.replace('.', '', 1).isdigit())))
            
    # Filter rows where all values in columns from 'F1961' to 'F2023' are decimal numbers
    valid_rows = is_decimal.all(axis=1)
    df = df[valid_rows]

    db_path = os.path.join("..", "data", "surface_temperature.db")
    save_to_sqlite(df, db_path, "surface_temperature")

    # Delete the CSV file after saving to the database
    os.remove(csv_filename)
