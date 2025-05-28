import mysql.connector
import pandas as pd

myConnection = mysql.connector.connect(
    user='root',
    password='$A!nts2497',
    host='localhost',
    database='ExchangeInfo'
)

cursorObject = myConnection.cursor()


df = pd.DataFrame({
    "AssetClassId": [1, 2, 3],
    "AssetClassName": ["Stock", "Option", "Future"]
})


df.columns = [col.replace(" ", "").replace("'", "") for col in df.columns]


data_list = df.to_records(index=False).tolist()


cursorObject.execute("""
CREATE TABLE IF NOT EXISTS AssetClass (
    AssetClassId INT PRIMARY KEY,
    AssetClassName VARCHAR(50) NOT NULL
)
""")

query = """
INSERT INTO AssetClass (
    AssetClassId,
    AssetClassName
) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE AssetClassName = VALUES(AssetClassName)
"""

cursorObject.executemany(query, data_list)
myConnection.commit()

print(f"Inserted {cursorObject.rowcount} total asset classes into AssetClass table.")

cursorObject.close()
myConnection.close()
