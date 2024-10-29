import requests
import pandas as pd

def calculate_margin_and_premium(data: pd.DataFrame, access_token: str, lot_size: int) -> pd.DataFrame:
    # Ensure the DataFrame has the necessary columns
    required_columns = ['instrument_name', 'strike_price', 'side', 'bid_ask']  # Adjust this according to your actual column names
    if not all(column in data.columns for column in required_columns):
        raise ValueError(f"DataFrame must contain the following columns: {required_columns}")
    
    # Initialize new columns
    data['margin_required'] = 0.0
    data['premium_earned'] = 0.0

    for index, row in data.iterrows():
        # Prepare the API request for margin calculation
        margin_url = 'https://api.upstox.com/v2/margin'  # Replace with actual margin calculation endpoint
        margin_params = {
            'instrument_name': row['instrument_name'],
            'strike_price': row['strike_price'],
            'side': row['side'],
            'transaction_type': 'Sell'
        }
        margin_headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Request margin requirement
        try:
            margin_response = requests.get(margin_url, params=margin_params, headers=margin_headers)
            margin_response.raise_for_status()
            margin_data = margin_response.json()
            data.at[index, 'margin_required'] = margin_data.get('margin_required', 0.0)  # Update with the correct key
        except requests.exceptions.RequestException as e:
            print(f"Error fetching margin data for row {index}: {e}")

        # Calculate premium earned
        bid_ask_price = row['bid_ask']  # Adjust this according to your actual DataFrame column name
        premium_earned = bid_ask_price * lot_size
        data.at[index, 'premium_earned'] = premium_earned

    return data

# Example usage
# Assuming you have your access token and a lot size defined
# lot_size = 50  # Replace with the actual lot size
# option_data = getOptionchain('NSE_INDEX|Nifty Bank', '2024-06-19', access_token)
# calculated_data = calculate_margin_and_premium(option_data, access_token, lot_size)