import requests
import geojson
import csv
import pandas as pd
import os
import sqlite3
import matplotlib.pyplot as plt


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

def preprocess_dates_co2(df):
    # Convert '1958M03' to '1958-03-01'
    df['Date'] = pd.to_datetime(df['Date'].apply(lambda x: f"{x[:4]}-{x[5:]}-01"), format='%Y-%m-%d')
    df = df[(df['Date'].dt.year >= 1961) & (df['Date'].dt.year <= 2023)]
    return df
    

def remove_f_prefix(df):
    cols_with_f = [col for col in df.columns if col.startswith('F')]
    df.rename(columns={col: col[1:] for col in cols_with_f}, inplace=True)
    return df

def plot_data(df_co2, df_temp):

    # Plot CO2 concentrations over time
    plt.figure(figsize=(10, 5))
    plt.plot(pd.to_datetime(df_co2['Date']), df_co2['Value'], label='CO2 Concentration (ppm)')
    plt.xlabel('Date')
    plt.ylabel('CO2 Concentration (ppm)')
    plt.title('Monthly Atmospheric CO2 Concentrations')
    plt.legend()
    plt.grid(True)
    plt.savefig('co2_concentrations.png')
    plt.show()

    # Melt the temperature dataframe
    value_vars = [col for col in df_temp.columns if col.isdigit()]
    df_temp_melted = df_temp.melt(id_vars=["Country", "Unit"], value_vars=value_vars, var_name="Year", value_name="Temperature")
    df_temp_melted['Year'] = df_temp_melted['Year'].astype(int)  # Convert year to integer

    # Aggregate the temperature data by year (average temperature across countries)
    df_temp_agg = df_temp_melted.groupby('Year')['Temperature'].mean().reset_index()

    # Plot global surface temperature over time
    plt.figure(figsize=(10, 5))
    plt.plot(df_temp_agg['Year'], df_temp_agg['Temperature'], label='Global Surface Temperature (°C)')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.title('Annual Mean Global Surface Temperature')
    plt.legend()
    plt.grid(True)
    plt.savefig('global_surface_temperature.png')
    plt.show()


if __name__ == "__main__":

    # Define the absolute path to the data directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    url = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Indicator_3_2_Climate_Indicators_Monthly_Atmospheric_Carbon_Dioxide_concentrations/FeatureServer/0/query?where=1=1&outFields=*&f=geojson"
    geojson_data = fetch_geojson_data(url)
    if geojson_data:
        # csv_filename = os.path.join("..", "data", "carbon_dioxide.csv")
        csv_filename = os.path.join(data_dir, "carbon_dioxide.csv")
        
        
        geojson_to_csv(geojson_data, csv_filename)

    df_co2 = pd.read_csv(csv_filename)

    # Drop the 'ISO2', 'ISO3', etc. (not needed columns) if they exist
    df_co2= df_co2.drop(columns=['ISO2', 'ISO3', 'Indicator', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor'], errors='ignore')
          
    # Ensure the 'Value' column is numeric 
    df_co2['Value'] = pd.to_numeric(df_co2['Value'], errors='coerce')

    # Drop rows with invalid 'Date' or 'Value'
    df_co2 = df_co2.dropna(subset=['Date', 'Value'])
    df_co2 = preprocess_dates_co2(df_co2)
    df_co2 = df_co2[df_co2['Unit'] == 'Parts Per Million']  # Filter for 'Parts Per Million' unit

    # db_path = os.path.join("..", "data", "carbon_dioxide.db")
    db_path = os.path.join(data_dir, "carbon_dioxide.db")
    save_to_sqlite(df_co2, db_path, "carbon_dioxide")

    # Delete the CSV file after saving to the database
    os.remove(csv_filename)
    
    url = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature/FeatureServer/0/query?where=1=1&outFields=*&f=geojson"
    geojson_data = fetch_geojson_data(url)
    if geojson_data:
        # csv_filename = os.path.join("..","data", "surface_temperature.csv")
        csv_filename = os.path.join(data_dir, "surface_temperature.csv")
        
        geojson_to_csv(geojson_data, csv_filename)

    df_temp = pd.read_csv(csv_filename)

    
    
    # Drop the 'ISO2', 'ISO3', etc. (not needed columns) if they exist
    df_temp = df_temp.drop(columns=['ISO2', 'ISO3', 'Indicator', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor'], errors='ignore')
    
    

    # Check if values in columns from 'F1961' to 'F2023' are decimal numbers
    cols_to_check = df_temp.loc[:, 'F1961':'F2023']
    is_decimal = cols_to_check.apply(lambda col: col.map(lambda x: isinstance(x, float) or (isinstance(x, str) and x.replace('.', '', 1).isdigit())))
            
    # Filter rows where all values in columns from 'F1961' to 'F2023' are decimal numbers
    valid_rows = is_decimal.all(axis=1)
    df_temp = df_temp[valid_rows]

    # Remove 'F' prefix from year columns
    df_temp = remove_f_prefix(df_temp)

    # db_path = os.path.join("..", "data", "surface_temperature.db")
    db_path = os.path.join(data_dir, "surface_temperature.db")
    save_to_sqlite(df_temp, db_path, "surface_temperature")

    # Delete the CSV file after saving to the database
    os.remove(csv_filename)

    plot_data(df_co2, df_temp)
