import os, pickle, pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import boto3
import toml

# # Set up AWS credentials

secrets = toml.load(".gitignore\secrets.toml")
print(secrets)
ACCESS_KEY = secrets['ACCESS_KEY']
SECRET_KEY = secrets['SECRET_KEY']

# List of Tickers:
list_of_tickers = ['AAPL','MSFT','AMZN','NVDA','GOOGL','GOOG','TSLA','META','BRK.B','XOM','UNH','LLY','JPM','V','JNJ','AVGO','PG','MA','HD','CVX','MRK','ADBE','ABBV','COST','PEP','CSCO', 'KO', 'WMT', 'CRM', 'TMO', 'ACN', 'MCD', 'NFLX', 'BAC', 'PFE', 'ORCL', 
'LIN', 'CMCSA', 'ABT', 'AMD', 'DHR', 'INTU', 'INTC', 'WFC', 'TXN', 'COP', 'DIS', 'CAT', 'PM', 'VZ', 'LOW', 'IBM', 'NEE', 'AMGN', 'UNP', 'SPGI', 'AMAT', 'QCOM', 'BMY', 'NKE', 'BA', 'HON', 'GE', 'RTX', 'NOW', 'UPS', 'BKNG', 'DE', 'PLD', 'SBUX', 'MS', 'ISRG',
 'MDT', 'GS', 'ELV', 'TJX', 'T', 'ADP', 'BLK', 'SYK', 'MMC', 'LMT', 'MDLZ', 'AXP', 'LRCX', 'GILD', 'ADI', 'ETN', 'VRTX', 'REGN', 'SCHW', 'SLB', 'ZTS', 'CVS', 'CB', 'AMT', 'CI', 'C', 'PGR', 'EOG', 'MO', 'BSX', 'TMUS', 'MU', 'FI', 'BDX', 'PANW', 'CME', 'SO', 'EQIX',
   'SNPS', 'KLAC', 'PYPL', 'AON', 'ITW', 'CDNS', 'DUK', 'ATVI', 'ICE', 'APD', 'SHW', 'MPC', 'CSX', 'NOC', 'CL', 'FDX', 'MMM', 'HUM', 'FCX', 'WM', 'ORLY', 'TGT', 'HCA', 'PXD', 'EMR', 'MCK', 'CMG', 'NXPI', 'PSX', 'MCO', 'PH', 'ROP', 'APH', 'MAR', 'USB', 'GD', 'ANET',
     'AJG', 'VLO', 'ADSK', 'F', 'AZO', 'PNC', 'CARR', 'OXY', 'MSI', 'TT', 'EW', 'TDG', 'GM', 'NSC', 'ECL', 'MCHP', 'HES', 'SRE', 'CHTR', 'MSCI', 'PCAR', 'AIG', 'ON', 'CTAS', 'CCI', 'MNST', 'NUE', 'ADM', 'PSA', 'KMB', 'STZ', 'TEL', 'ROST', 'DXCM', 'WMB', 'AFL', 
     'WELL', 'MET', 'IQV', 'IDXX', 'FTNT', 'HLT', 'EXC', 'JCI', 'TFC', 'AEP', 'CPRT', 'GIS', 'COF', 'DOW', 'PAYX', 'KVUE', 'ODFL', 'D', 'BIIB', 'DLR', 'SPG', 'BKR', 'O', 'HAL', 'TRV', 'CTSH', 'EL', 'DHI', 'AME', 'CTVA', 'AMP', 'MRNA', 'YUM', 'ROK', 'VRSK', 'OTIS',
       'CNC', 'A', 'CEG', 'DD', 'SYY', 'PRU', 'DVN', 'CSGP', 'GPN', 'CMI', 'URI', 'KMI', 'FIS', 'LHX', 'BK', 'PPG', 'FAST', 'EA', 'GWW', 'VICI', 'HSY', 'XEL', 'NEM', 'ED', 'WST', 'PWR', 'LEN', 'RSG', 'KR', 'PEG', 'CDW', 'FANG', 'ALL', 'VMC', 'OKE', 'IR', 'COR', 
       'ACGL', 'KDP', 'ANSS', 'DG', 'APTV', 'IT', 'FTV', 'MLM', 'CBRE', 'EXR', 'DAL', 'MTD', 'PCG', 'ALGN', 'GEHC', 'AWK', 'HPQ', 'WEC', 'EIX', 'KHC', 'ZBH', 'WBD', 'LYB', 'ILMN', 'AVB', 'TROW', 'EFX', 'DLTR', 'GLW', 'KEYS', 'WY', 'EBAY', 'TSCO', 'SBAC', 'MPWR',
         'STT', 'XYL', 'DFS', 'CHD', 'HPE', 'FICO', 'CAH', 'RMD', 'TTWO', 'HIG', 'ALB', 'STE', 'WTW', 'BR', 'EQR', 'RCL', 'GPC', 'CTRA', 'ES', 'DTE', 'ULTA', 'FLT', 'RJF', 'MTB', 'DOV', 'AEE', 'MKC', 'BAX', 'WAB', 'ETR', 'INVH', 'TDY', 'TRGP', 'NVR', 'CLX', 'FE', 
         'VRSN', 'IRM', 'HOLX', 'ARE', 'FITB', 'DRI', 'LH', 'IFF', 'FSLR', 'MOH', 'PHM', 'HWM', 'LUV', 'EXPD', 'PPL', 'COO', 'NDAQ', 'NTAP', 'PFG', 'CNP', 'LVS', 'BRO', 'VTR', 'RF', 'J', 'SWKS', 'MRO', 'ENPH', 'STLD', 'IEX', 'BG', 'CINF', 'BALL', 'TER', 'FDS', 
         'OMC', 'MAA', 'WAT', 'TYL', 'WBA', 'ATO', 'CMS', 'GRMN', 'CF', 'AKAM', 'UAL', 'CBOE', 'NTRS', 'EG', 'HBAN', 'PTC', 'EXPE', 'CCL', 'JBHT', 'EQT', 'TXT', 'K', 'ESS', 'SJM', 'AXON', 'AVY', 'EPAM', 'TSN', 'BBY', 'WDC', 'SWK', 'PAYC', 'DGX', 'RVTY', 'ZBRA', 
         'SNA', 'AMCR', 'SYF', 'STX', 'LW', 'APA', 'CAG', 'DPZ', 'POOL', 'CFG', 'PODD', 'TRMB', 'MGM', 'LDOS', 'KMX', 'PKG', 'MOS', 'MAS', 'LKQ', 'NDSN', 'MTCH', 'CE', 'IPG', 'WRB', 'LNT', 'VTRS', 'EVRG', 'L', 'UDR', 'TECH', 'IP', 'INCY', 'AES', 'GEN', 'TAP', 
         'CPT', 'BF.B', 'HST', 'LYV', 'PNR', 'CZR', 'KIM', 'CDAY', 'PEAK', 'JKHY', 'HRL', 'QRVO', 'NI', 'CRL', 'KEY', 'FMC', 'CHRW', 'HSIC', 'WYNN', 'EMN', 'TFX', 'REG', 'GL', 'FFIV', 'BWA', 'ALLE', 'JNPR', 'AAL', 'BXP', 'HAS', 'AOS', 'ETSY', 'CTLT', 'NRG', 'ROL',
           'SEDG', 'MKTX', 'BBWI', 'FOXA', 'PNW', 'CPB', 'HII', 'NWSA', 'UHS', 'WRK', 'RHI', 'XRAY', 'BIO', 'TPR', 'WHR', 'BEN', 'GNRC', 'AIZ', 'FRT', 'IVZ', 'NCLH', 'PARA', 'VFC', 'CMA', 'DVA', 'ZION', 'SEE', 'ALK', 'OGN', 'MHK', 'RL', 'DXC', 'FOX', 'LNC', 'NWL',
             'NWS', 'FTRE']

# This function gets the dataframe used for equity prices
def get_dataframe_eq(ticker: str) -> str:
    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
        # aws_session_token=SESSION_TOKEN
    )

    # Specify the bucket name and file name
    bucket_name = 'intraday-dashboard'
    file_name = 'eq_'+ticker+'.csv'

    # Download the file from the S3 bucket
    s3.download_file(bucket_name, file_name, file_name)

    # Process the file as needed

    df = pd.read_csv(file_name)


    # print(df)
    return df

def strike_prices_to_display(strike_list, close_price):
    result = []
    for element in strike_list:
        if close_price*0.8 < element < close_price*1.2:
            result.append(element)
    return result

def get_dataframe_opt(ticker: str):
    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
        # aws_session_token=SESSION_TOKEN
    )

    # Specify the bucket name and file name
    bucket_name = 'intraday-dashboard'
    file_name = 'opt_'+ticker+'.csv'

    # Download the file from the S3 bucket
    s3.download_file(bucket_name, file_name, file_name)

    # Process the file as needed

    df = pd.read_csv(file_name)


    # print(df)
    return df