import mysql.connector
import pandas as pd


myConnection = mysql.connector.connect(
    user='root',
    password='$A!nts2497',
    host='localhost',
    database='ExchangeInfo'
)
cursorObject = myConnection.cursor()


EXCHANGE_IDS = {
    'NYSE': 1,
    'NASDAQ': 2,
    'CBOE': 3,
    'CBOE BZX': 4,
    'CBOE BYX': 5,
    'CBOE EDGA': 6,
    'CBOE EDGX': 7,
    'CBOE C2': 8,
    'IEX': 9,
    'MIAX': 10,
    'CME': 11
}


nasdaq_df = pd.read_csv("nasdaq-listed.csv")
nyse_df = pd.read_csv("nyse-listed.csv")
nasdaq_df['ExchangeId'] = EXCHANGE_IDS['NASDAQ']
nyse_df['ExchangeId'] = EXCHANGE_IDS['NYSE']
stock_df = pd.concat([nasdaq_df, nyse_df], ignore_index=True)
stock_df['Symbol'] = stock_df['Symbol'].combine_first(stock_df['ACT Symbol'])
stock_df['Product_Name'] = stock_df['Security Name'].combine_first(stock_df['Company Name'])
stock_df = stock_df.dropna(subset=['Symbol', 'Product_Name'])
stock_df = stock_df[stock_df['Symbol'].astype(str).str.strip() != '']
stock_df = stock_df[stock_df['Product_Name'].astype(str).str.strip() != '']
stock_df['Symbol'] = stock_df['Symbol'].astype(str).str.strip().str[:20]
stock_df['Contract_Type'] = 'Stock'
stock_df['Asset_Class_Id'] = 1
stock_df = stock_df[['Symbol', 'Contract_Type', 'Product_Name', 'Asset_Class_Id', 'ExchangeId']]


miax_pearl_df = pd.read_csv("MIAXPEARLListingsClasses.csv")
miax_pearl_df = miax_pearl_df[['Options Symbol', 'Underlying Name']]
miax_pearl_df = miax_pearl_df.dropna(subset=['Options Symbol', 'Underlying Name'])
miax_pearl_df = miax_pearl_df[miax_pearl_df['Options Symbol'].astype(str).str.strip() != '']
miax_pearl_df = miax_pearl_df[miax_pearl_df['Underlying Name'].astype(str).str.strip() != '']
miax_pearl_df['Symbol'] = miax_pearl_df['Options Symbol'].astype(str).str[:20]
miax_pearl_df['Product_Name'] = miax_pearl_df['Underlying Name']
miax_pearl_df['Contract_Type'] = 'Option'
miax_pearl_df['Asset_Class_Id'] = 2
miax_pearl_df['ExchangeId'] = EXCHANGE_IDS['MIAX']
miax_pearl_df = miax_pearl_df[['Symbol', 'Contract_Type', 'Product_Name', 'Asset_Class_Id', 'ExchangeId']]


def load_cboe_csv(path, exchange_id, has_header=True):
    if has_header:
        df = pd.read_csv(path, usecols=['Symbol', 'Company'])
        df.rename(columns={'Company': 'Product_Name'}, inplace=True)
    else:
        df = pd.read_csv(path, header=None, names=['Symbol', 'Product_Name'])
    df = df.dropna(subset=['Symbol', 'Product_Name'])
    df['Symbol'] = df['Symbol'].astype(str).str.strip().str[:20]
    df['Product_Name'] = df['Product_Name'].astype(str).str.strip()
    df = df[df['Symbol'] != '']
    df = df[df['Product_Name'] != '']
    df['Contract_Type'] = 'Option'
    df['Asset_Class_Id'] = 2
    df['ExchangeId'] = exchange_id
    return df[['Symbol', 'Contract_Type', 'Product_Name', 'Asset_Class_Id', 'ExchangeId']]

def load_symbol_only_csv(path, exchange_id, symbol_col='Symbols', contract_type='Stock', asset_class_id=0):
    df = pd.read_csv(path, usecols=[symbol_col])
    df = df.dropna(subset=[symbol_col])
    df['Symbol'] = df[symbol_col].astype(str).str.strip().str[:20]
    df = df[df['Symbol'] != '']
    df['Product_Name'] = df['Symbol']
    df['Contract_Type'] = contract_type
    df['Asset_Class_Id'] = asset_class_id
    df['ExchangeId'] = exchange_id
    return df[['Symbol', 'Contract_Type', 'Product_Name', 'Asset_Class_Id', 'ExchangeId']]


cboe_bzx_df = load_cboe_csv("CBOE_BZX.csv", EXCHANGE_IDS['CBOE BZX'])
cboe_c2_df = load_cboe_csv("CBOE_C2.csv", EXCHANGE_IDS['CBOE C2'])
cboe_edgx_df = load_cboe_csv("CBOE_EDGX.csv", EXCHANGE_IDS['CBOE EDGX'])
cboe_main_df = load_cboe_csv("CBOE.csv", EXCHANGE_IDS['CBOE'], has_header=False)
cboe_byx_df = load_symbol_only_csv("CBOE_BYX.csv", EXCHANGE_IDS['CBOE BYX'])
cboe_edga_df = load_symbol_only_csv("CBOE_EDGA.csv", EXCHANGE_IDS['CBOE EDGA'])

iex_df = pd.read_csv("IEX.csv", header=None, names=['Symbol', 'Date', 'Product_Name'])
iex_df = iex_df.dropna(subset=['Symbol', 'Product_Name'])
iex_df['Symbol'] = iex_df['Symbol'].astype(str).str.strip().str[:20]
iex_df['Product_Name'] = iex_df['Product_Name'].astype(str).str.strip()
iex_df = iex_df[iex_df['Symbol'] != '']
iex_df = iex_df[iex_df['Product_Name'] != '']
iex_df['Contract_Type'] = 'Stock'
iex_df['Asset_Class_Id'] = 1
iex_df['ExchangeId'] = EXCHANGE_IDS['IEX']
iex_df = iex_df[['Symbol', 'Contract_Type', 'Product_Name', 'Asset_Class_Id', 'ExchangeId']]


cme_df = pd.read_csv("CME_Cleaned.csv")
cme_df = cme_df.dropna(subset=['Symbol', 'Product_Name'])
cme_df['Symbol'] = cme_df['Symbol'].astype(str).str.strip().str[:20]
cme_df['Product_Name'] = cme_df['Product_Name'].astype(str).str.strip()
cme_df = cme_df[cme_df['Symbol'] != '']
cme_df = cme_df[cme_df['Product_Name'] != '']
cme_df['Asset_Class_Id'] = cme_df['Asset_Class_Id'].astype(int)
cme_df['ExchangeId'] = EXCHANGE_IDS['CME']
cme_df = cme_df[['Symbol', 'Contract_Type', 'Product_Name', 'Asset_Class_Id', 'ExchangeId']]


cboe_combined_df = pd.concat([
    cboe_bzx_df,
    cboe_c2_df,
    cboe_edgx_df,
    cboe_main_df,
    cboe_byx_df,
    cboe_edga_df
], ignore_index=True)

final_df = pd.concat([
    stock_df,
    miax_pearl_df,
    cboe_combined_df,
    iex_df,
    cme_df
], ignore_index=True)


final_df = final_df.drop_duplicates(subset=['Symbol', 'Asset_Class_Id', 'ExchangeId'])


data_list = final_df.to_records(index=False).tolist()

query = """
INSERT IGNORE INTO Product (
    Symbol,
    Contract_Type,
    Product_Name,
    Asset_Class_Id,
    ExchangeId
) VALUES (%s, %s, %s, %s, %s)
"""

cursorObject.executemany(query, data_list)
myConnection.commit()
print(f"Inserted {cursorObject.rowcount} total products into Product table.")

cursorObject.close()
myConnection.close()
