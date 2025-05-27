import mysql.connector
import pandas as pd

# Connect to the database
myConnection = mysql.connector.connect(
    user='root',
    password='$A!nts2497',
    host='localhost',
    database='ExchangeInfo'
)

cursorObject = myConnection.cursor()

# Read CSV with index_col=False
df = pd.read_csv("Databases Project Data - Exchange's.csv", index_col=False)

# Rename columns explicitly
df = df.rename(columns={
    "ExchangeId": "ExchangeId",
    "Exchange Name": "ExchangeName",
    "Address": "Address",
    "Trading Hours": "TradingHours",
    "Time Zone": "TimeZone",
    "Has Physical Trading Floor": "HasPhysicalTradingFloor"
})

# Ensure correct column order
expected_columns = ['ExchangeId', 'ExchangeName', 'Address', 'TradingHours', 'TimeZone', 'HasPhysicalTradingFloor']
df = df[expected_columns]

# Convert to list of tuples
data_list = df.to_records(index=False).tolist()

# Debug output
print(f"Sample row: {data_list[0]}")
print(f"Length of first row: {len(data_list[0])}")

# Insert query
query = """
INSERT INTO Exchange (
    ExchangeId,
    ExchangeName,
    Address,
    TradingHours,
    TimeZone,
    HasPhysicalTradingFloor
) VALUES (%s, %s, %s, %s, %s, %s)
"""

cursorObject.executemany(query, data_list)
myConnection.commit()

print(f"Inserted {cursorObject.rowcount} total exchanges into Exchange table.")

cursorObject.close()
myConnection.close()
