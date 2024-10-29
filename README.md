# Stock-Margin

Stock-Margin is a Python tool that leverages financial data from Upstox APIs to calculate margin requirements and premium earnings for options trading. It fetches option chain data for a given instrument and expiry date, computes margin and premium values, and exports the data to Excel for easy reference.

## Project Structure

The project consists of two main files:

1. **`calculate_margin_and_premium.py`**  
   - Fetches margin requirements and calculates premium earned based on lot size.
   - Requires an Upstox API access token and instrument details as inputs.

2. **`get_option_chain.py`**
   - Retrieves option chain data using Upstox API and formats it into a structured DataFrame.
   - Exports the option chain data to an Excel sheet for analysis.

## Code Logic & Approach

### `calculate_margin_and_premium.py`

1. **Validate Input Data:** Ensures necessary columns are present in the DataFrame.
2. **API Request:** Sends a request to fetch margin requirements for each row in the DataFrame, which includes details like `instrument_name`, `strike_price`, and `side`.
3. **Premium Calculation:** Computes premium earned based on `bid_ask` and `lot_size`.
4. **Return Data:** The function returns the DataFrame with additional columns for margin and premium values.

### `get_option_chain.py`

1. **API Request:** Retrieves option chain data for the specified instrument and expiry date from Upstox.
2. **Data Processing:** Extracts option chain information, including Greeks (Delta, Gamma, Vega, Theta, etc.), and stores them in a structured DataFrame.
3. **Excel Export:** Writes the option chain data to an Excel sheet using `xlwings`.

## Usage

To use the functions, ensure your environment is configured as follows:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Configure environment variables by creating a .env file and providing your API access token.

3. Run the scripts:
     ```
       from calculate_margin_and_premium import calculate_margin_and_premium
       from get_option_chain import getOptionchain

## Environment Variables Example:
   Create an .env file in the project root with the following structure:

       UPSTOX_ACCESS_TOKEN=your_access_token_here


## Dependencies:
   All dependencies are listed in requirements.txt. Key libraries include:
   
   *  requests: For API requests.
   *  pandas: For data manipulation.
   *  xlwings: For exporting data to Excel.

