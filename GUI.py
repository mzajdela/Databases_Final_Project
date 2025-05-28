import mysql.connector
import tkinter as tk

def create_connection(user: str, password: str, host='localhost', database=""):
    myConnection = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = myConnection.cursor()
    return myConnection, cursor

def close_connection(cursor, myConnection) -> None:
    cursor.close()
    myConnection.close()

def run_query(numQuery: str) -> str:
    myConnection, cursor = create_connection('root', '$A!nts2497', 'localhost', 'ExchangeInfo')
    try:
        numQuery = int(numQuery)
    except ValueError:
        return "Invalid input. Please enter a number."

    result = ""

    if numQuery == 1:
        query = """
            SELECT COUNT(DISTINCT p.Symbol) AS NumFuturesOnlyOnCME
            FROM Product p
            JOIN Exchange e ON p.ExchangeId = e.ExchangeId
            WHERE e.ExchangeName = 'CME'
              AND p.Contract_Type = 'Future'
              AND p.Symbol NOT IN (
                  SELECT Symbol
                  FROM Product
                  WHERE Contract_Type = 'Option'
                    AND ExchangeId = e.ExchangeId
              );
        """
        cursor.execute(query)
        result += f"Number of CME futures not listed as options: {cursor.fetchone()[0]}\n"

    elif numQuery == 2:
        query = """
            SELECT DISTINCT e.ExchangeName
            FROM Product p
            JOIN Exchange e ON p.ExchangeId = e.ExchangeId
            WHERE p.Symbol = 'AAPL'
              AND NOT EXISTS (
                  SELECT 1
                  FROM Product p2
                  WHERE p2.Symbol = 'ZBRA'
                    AND p2.ExchangeId = e.ExchangeId
              );
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Exchange = {row[0]}\n"

    elif numQuery == 3:
        query = """
            SELECT p.Contract_Type, COUNT(DISTINCT p.Symbol) AS UniqueSymbolCount
            FROM Product p
            JOIN Exchange e ON p.ExchangeId = e.ExchangeId
            WHERE e.ExchangeName = 'CME'
            GROUP BY p.Contract_Type;
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Contract Type = {row[0]}\nUnique Symbols = {row[1]}\n\n"

    elif numQuery == 4:
        query = """
            SELECT ExchangeName
            FROM Exchange
            WHERE Address LIKE '%Chicago%'
               OR Address LIKE '%New York%';
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Exchange Name = {row[0]}\n"

    elif numQuery == 5:
        query = """
            SELECT COUNT(*) AS num_single_exchange_products
            FROM (
                SELECT Symbol
                FROM Product
                GROUP BY Symbol
                HAVING COUNT(*) = 1
            ) AS single_listings;
        """
        cursor.execute(query)
        result += f"Number of products listed on only one exchange: {cursor.fetchone()[0]}\n"

    elif numQuery == 6:
        query = """
            SELECT e.ExchangeName, r.Regulator_Name, p.Symbol AS Listed_Symbol
            FROM Product p
            JOIN Exchange e ON p.ExchangeId = e.ExchangeId
            JOIN Is_Supervised_By isb ON e.ExchangeId = isb.ExchangeId
            JOIN Regulators r ON isb.Regulator_ID = r.Regulator_ID
            WHERE r.Regulator_ID = 1 AND p.Symbol = 'TRIP';
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Exchange = {row[0]}\nRegulator = {row[1]}\nSymbol = {row[2]}\n\n"

    elif numQuery == 7:
        query = """
            SELECT e.ExchangeName, COUNT(o.HolidayId) AS HolidayCount
            FROM ExchangeInfo.Exchange AS e
            JOIN ExchangeInfo.Is_Observed_By AS o ON e.ExchangeId = o.ExchangeId
            JOIN ExchangeInfo.Holidays AS h ON o.HolidayId = h.HolidayId
            WHERE h.HolidayDate >= '2025-06-01' AND h.HolidayDate < '2025-09-01' AND h.IsEarlyClose = True
            GROUP BY e.ExchangeName;
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Exchange Name = {row[0]}\nEarly Close Holidays = {row[1]}\n\n"

    elif numQuery == 8:
        query = """
            SELECT h.HolidayName, h.HolidayDate
            FROM ExchangeInfo.Holidays AS h
            JOIN ExchangeInfo.Is_Observed_By AS o ON h.HolidayId = o.HolidayId
            JOIN ExchangeInfo.Exchange AS e ON e.ExchangeId = o.ExchangeId
            WHERE e.ExchangeName = 'CBOE'
              AND NOT EXISTS (
                  SELECT 1
                  FROM ExchangeInfo.Holidays AS h2
                  JOIN ExchangeInfo.Is_Observed_By AS o2 ON h2.HolidayId = o2.HolidayId
                  JOIN ExchangeInfo.Exchange AS e2 ON e2.ExchangeId = o2.ExchangeId
                  WHERE e2.ExchangeName = 'CME' AND h2.HolidayName = h.HolidayName AND h2.HolidayDate = h.HolidayDate
              );
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Holiday Name = {row[0]}\nHoliday Date = {row[1]}\n\n"

    elif numQuery == 9:
        query = """
            SELECT b.CIK, CompanyName
            FROM Broker_Dealer AS b
            INNER JOIN Is_A_Member_Of AS m ON b.CIK = m.CIK
            WHERE Is_DPM = 0 AND ExchangeId = 1
              AND b.CIK NOT IN (
                  SELECT b2.CIK
                  FROM Broker_Dealer AS b2
                  INNER JOIN Is_A_Member_Of AS m2 ON b2.CIK = m2.CIK
                  WHERE Is_DPM = 0 AND ExchangeId = 2
              );
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"CIK = {row[0]}\nCompany Name = {row[1]}\n\n"

    elif numQuery == 10:
        query = """
            SELECT b.CompanyName, b.CompanyAddress, COUNT(DISTINCT h.HolidayId) AS Num_Full_Holidays
            FROM Is_A_Member_Of AS m
            INNER JOIN Broker_Dealer AS b ON m.CIK = b.CIK
            INNER JOIN Is_Observed_By AS o ON m.ExchangeId = o.ExchangeId
            INNER JOIN Holidays AS h ON o.HolidayId = h.HolidayId
            WHERE h.IsEarlyClose = False AND m.Is_DPM = 1
            GROUP BY b.CompanyName, b.CompanyAddress
            HAVING Num_Full_Holidays = 10;
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Company Name = {row[0]}\nCompany Address = {row[1]}\nFull Holidays Observed = {row[2]}\n\n"

    else:
        result = "Incorrect entry. Please enter a number 1–10 to display query results."

    close_connection(cursor, myConnection)
    return result

def insert_exchange(input: str) -> str:
    try:
        name, address, time_zone, has_trading_floor, trading_hours = [s.strip() for s in input.split(',')]
        values = (name, address, time_zone, has_trading_floor, trading_hours)
        myConnection, cursor = create_connection('root', '$A!nts2497', 'localhost', 'ExchangeInfo')
        cursor.execute(
            """
            INSERT INTO ExchangeInfo.Exchange(ExchangeName, Address, TimeZone, HasPhysicalTradingFloor, TradingHours)
            VALUES (%s, %s, %s, %s, %s);
            """,
            values
        )
        myConnection.commit()
        return f"Successfully inserted exchange {name}!"
    except Exception:
        return f"Error inserting Exchange {name}"
    finally:
        close_connection(cursor, myConnection)

def insert_asset_class(name: str) -> str:
    try:
        myConnection, cursor = create_connection('root', '$A!nts2497', 'localhost', 'ExchangeInfo')
        cursor.execute(
            """
            INSERT INTO ExchangeInfo.AssetClass(AssetClassName) VALUES (%s);
            """,
            (name,)
        )
        myConnection.commit()
        return f"Successfully inserted asset class {name}!"
    except Exception:
        return f"Error adding new AssetClass {name}"
    finally:
        close_connection(cursor, myConnection)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Exchange Database Explorer")
        # Welcome Message
    welcome_label = tk.Label(
        root,
        text="Welcome to our Exchange Database Explorer!\n"
             "Use this tool to run predefined SQL queries against the ExchangeInfo database\n"
             "and add asset classes and exchange metadata via the interface below.",
        font=("Arial", 10, "italic"),
        justify="left",
        padx=10,
        pady=5,
        anchor="w"
    )
    welcome_label.pack(fill=tk.X)

    query_list_text = (
        "Query List\n\n"
        "1. Count the number of symbols listed on the CME that are futures but not options.\n"
        "2. Display all exchanges that have AAPL listed but do not have ZBRA listed.\n"
        "3. Display the number of unique symbols for each contract type that trade at the CME.\n"
        "4. Display all exchanges located in either Chicago or New York.\n"
        "5. Count how many products are listed on only one exchange.\n"
        "6. Display all exchanges supervised by the SEC that have TRIP listed.\n"
        "7. Count the number of early close holidays per exchange between June and September 2025.\n"
        "8. Display holidays (name and date) observed by CBOE but not by CME.\n"
        "9. List non-DPM Broker Dealers who are members of NYSE but not NASDAQ.\n"
        "10. Find DPMs who observe exactly 10 full holidays (not early close).\n"
    )

    top_frame = tk.Frame(root, padx=10, pady=10)
    top_frame.pack(fill=tk.X)

    query_label = tk.Label(top_frame, text=query_list_text, anchor="w", justify="left")
    query_label.pack(anchor="w")

    input_frame = tk.Frame(top_frame)
    input_frame.pack(anchor="w")

    tk.Label(input_frame, text="Enter query number (1–10):").pack(side=tk.LEFT)
    query_input = tk.Entry(input_frame, width=5)
    query_input.pack(side=tk.LEFT, padx=5)

    middle_frame = tk.Frame(root, padx=10, pady=10)
    middle_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(middle_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_text = tk.Text(middle_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=20, width=80)
    result_text.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=result_text.yview)

    # NEW: Status message below the scrollable result box
    status_label = tk.Label(root, text="", fg="blue", anchor="w", justify="left")
    status_label.pack(fill=tk.X, padx=10)

    def run_and_display():
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, run_query(query_input.get()))

    tk.Button(input_frame, text="Run Query", command=run_and_display).pack(side=tk.LEFT, padx=5)

    bottom_frame = tk.Frame(root, padx=10, pady=10)
    bottom_frame.pack(fill=tk.X)

    tk.Label(bottom_frame, text="Insert Asset Class (name(string):").grid(row=0, column=0, sticky="e")
    asset_class_entry = tk.Entry(bottom_frame)
    asset_class_entry.grid(row=0, column=1, padx=5)
    tk.Button(bottom_frame, text="Submit", command=lambda: status_label.config(text=insert_asset_class(asset_class_entry.get()))).grid(row=0, column=2, padx=5)

    tk.Label(bottom_frame, text="Insert Exchange (name(string),address(string),timezone(string),hasTradingFloor(int 0/1),hours(string, ie: 09:30a-04:00p)):").grid(row=1, column=0, sticky="e")
    exchange_entry = tk.Entry(bottom_frame, width=60)
    exchange_entry.grid(row=1, column=1, padx=5)
    tk.Button(bottom_frame, text="Submit", command=lambda: status_label.config(text=insert_exchange(exchange_entry.get()))).grid(row=1, column=2, padx=5)

    root.mainloop()
