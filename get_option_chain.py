import requests
import pandas as pd
import xlwings as xw

def getOptionchain(ik, expiry, access_token):
    url = 'https://api.upstox.com/v2/option/chain'
    params = {
        "mode": "option_chain",
        'instrument_key': ik,
        'expiry_date': expiry
    }
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Make the API request
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    option_chain = response.json().get('data', [])
    optionchain = pd.DataFrame(columns=[
        'call_vol', 'call_iv', 'call_vega', 'call_gamma', 'call_theta',
        'call_delta', 'call_prev_oi', 'call_oi', 'call_ltp', 'strike',
        'put_ltp', 'put_oi', 'put_prev_oi', 'put_delta', 'put_theta',
        'put_gamma', 'put_vega', 'put_iv', 'put_vol'
    ])
    
    # Iterate through the option chain data
    records = []
    for x in option_chain:
        call_data = x['call_options']['market_data']
        put_data = x['put_options']['market_data']
        call_greeks = x['call_options']['option_greeks']
        put_greeks = x['put_options']['option_greeks']
        
        record = [
            call_data['volume'], call_greeks['iv'], call_greeks['vega'], call_greeks['gamma'],
            call_greeks['theta'], call_greeks['delta'], call_data['prev_oi'], call_data['oi'],
            call_data['ltp'], x['strike_price'], put_data['ltp'], put_data['oi'],
            put_data['prev_oi'], put_greeks['delta'], put_greeks['theta'], put_greeks['gamma'],
            put_greeks['vega'], put_greeks['iv'], put_data['volume']
        ]
        records.append(record)

    # Create DataFrame from the records
    optionchain = pd.DataFrame(records, columns=optionchain.columns)

    # Write to Excel
    try:
        excel_obj = xw.Book('oc.xlsx')
        data = excel_obj.sheets['opchain']
        data.range('a1:z500').value = None  # Clear previous data
        data.range('a1').value = optionchain.values  # Write new data
    except Exception as e:
        print(f"Error writing to Excel: {e}")

# Call the function
# Make sure to pass your access token
# getOptionchain('NSE_INDEX|Nifty Bank', '2024-06-19', 'your_access_token')

# done 