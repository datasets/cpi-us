import os
import requests
import pandas as pd
from datetime import datetime

archive_path = 'archive/cpiai_archived.csv'
output_path = 'data/cpiai.csv'

api_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
api_key = os.getenv("BLS_API_KEY") # Replace with your actual API key

# Specify the series ID and the date range
series_id = "CUUR0000SA0"  # CPI-U All Items for U.S. City Average, not seasonally adjusted
start_year = 2014
end_year = datetime.now().year + 1

# Prepare the request payload with the API key
headers = {'Content-type': 'application/json'}
payload = {
    "seriesid": [series_id],
    "startyear": str(start_year),
    "endyear": str(end_year),
    "registrationkey": api_key
}

def get_cpi_data():
    response = requests.post(api_url, json=payload, headers=headers)
    json_data = response.json()

    # Check if the request was successful
    if response.status_code == 200 and json_data["status"] == "REQUEST_SUCCEEDED":
        # Extract the data
        cpi_data = []
        for series in json_data["Results"]["series"]:
            for item in series["data"]:
                year = int(item["year"])
                period = item["period"]
                value = float(item["value"])
                if period.startswith('M'):
                    month = int(period[1:])
                    date = datetime(year, month, 1)
                    cpi_data.append([date, value])

        df = pd.DataFrame(cpi_data, columns=["Date", "CPI"])
        df = df.sort_values(by="Date").reset_index(drop=True)

        # Calculate the monthly inflation rate
        df["Inflation"] = df["CPI"].pct_change() * 100
        df["Inflation"] = df["Inflation"].round(2)

        return df
    else:
        print(f"Error: {json_data.get('message', 'Unknown error')}")
        return None

def process():
    # Get new CPI data
    new_data = get_cpi_data()
    new_data = new_data.iloc[1:].copy()

    # Check if there is data to merge
    if new_data is not None and not new_data.empty:
        # Load the archived CPI data
        archive_df = pd.read_csv(archive_path, parse_dates=['Date'])
        archive_df.columns = ['Date', 'CPI', 'Inflation']

        # Combine the archived data with the modified new data
        merged_df = pd.concat([archive_df, new_data], ignore_index=True)

        # Sort by Date to ensure chronological order and fill NaN values with empty strings
        merged_df = merged_df.sort_values(by='Date').reset_index(drop=True)
        merged_df = merged_df.fillna('')

        # Save the final merged DataFrame to output_path
        merged_df.to_csv(output_path, index=False)
        print("Data updated successfully!")
    else:
        print("Failed to update the data.")

if __name__ == '__main__':
    process()
