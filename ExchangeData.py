import mysql.connector
import pandas as pd


myConnection = mysql.connector.connect(
    user='root',
    password='$A!nts2497',
    host='localhost',
    database='ExchangeInfo'
)

cursorObject = myConnection.cursor()


df = pd.read_csv("Databases Project Data - Exchange's.csv")


df = df.rename(columns={
    "Exchange Name": "ExchangeName",
    "Trading Hours": "TradingHours",
    "Has Physical Trading Floor": "HasPhysicalTradingFloor"
})
df.columns = [col.replace(" ", "").replace("'", "") for col in df.columns]


data_list = df.to_records(index=False).tolist()


query = """
INSERT INTO Exchange (
    ExchangeName,
    Address,
    TradingHours,
    TimeZone,
    HasPhysicalTradingFloor
) VALUES (%s, %s, %s, %s, %s)
"""

cursorObject.executemany(query, data_list)
myConnection.commit()

print(f"Inserted {cursorObject.rowcount} total exchanges into Exchange table.")

cursorObject.close()
myConnection.close()
