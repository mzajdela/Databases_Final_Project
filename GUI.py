import mysql.connector
import tkinter as tk

def create_connection(user: str, password: str, host='localhost', database=""):
    """
    Creates connector object with MySql and creates curser object

    Parameters:
        user: (str) MySql username
        password: (str) MySql password
        host: (str) MySql host, defaulted to localhost
        database: (str) The database you are trying to connect to. Optional parameter

    Returns:
        Connector object and Curser object
    """
    if database:
        myConnection = mysql.connector.connect(user=user, password=password, host=host, database=database)
    else:
        myConnection = mysql.connector.connect(user=user, password=password, host=host)
    cursor = myConnection.cursor()

    return myConnection, cursor

def close_connection(cursor, myConnection) -> None:
    """
    Closes MySql connection and curser connection.

    Parameters:
        cursor: cursor object
        myConnection: MySql connection object

    Returns:
        None
    """
    cursor.close()
    myConnection.close()

def run_query(numQuery: str) -> str:
    """
    This method runs the selected query and returns the results in the GUI.

    Parameters:
        numQuery: str passed in from Query text box

    Returns: (str) Query Results
    """
    # Create MySQL Connection
    myConnection, cursor = create_connection('root', '$A!nts2497', 'localhost', 'ExchangeInfo')
    numQuery = int(numQuery)
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
            result += f"Contract Type = {row[0]}\n"
            result += f"Unique Symbols = {row[1]}\n\n"

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
            SELECT 
                e.ExchangeName,
                r.Regulator_Name,
                p.Symbol AS Listed_Symbol
            FROM 
                Product p
            JOIN Exchange e ON p.ExchangeId = e.ExchangeId
            JOIN Is_Supervised_By isb ON e.ExchangeId = isb.ExchangeId
            JOIN Regulators r ON isb.Regulator_ID = r.Regulator_ID
            WHERE 
                r.Regulator_ID = 1
                AND p.Symbol = 'TRIP';
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Exchange = {row[0]}\n"
            result += f"Regulator = {row[1]}\n"
            result += f"Symbol = {row[2]}\n\n"

    elif numQuery == 7:
        query = """
            SELECT e.ExchangeName, COUNT(o.HolidayId) AS HolidayCount
            FROM ExchangeInfo.Exchange AS e
            JOIN ExchangeInfo.Is_Observed_By AS o ON e.ExchangeId = o.ExchangeId
            JOIN ExchangeInfo.Holidays AS h ON o.HolidayId = h.HolidayId
            WHERE h.HolidayDate >= '2025-06-01'
              AND h.HolidayDate < '2025-09-01'
              AND h.IsEarlyClose = True
            GROUP BY e.ExchangeName;
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Exchange Name = {row[0]}\n"
            result += f"Early Close Holidays (June–August 2025) = {row[1]}\n\n"

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
                    WHERE e2.ExchangeName = 'CME'
                    AND h2.HolidayName = h.HolidayName
                    AND h2.HolidayDate = h.HolidayDate
                );
        """
        cursor.execute(query)
        query_results = cursor.fetchall()
        for row in query_results:
            result += f"Holiday Name = {row[0]}\n"
            result += f"Holiday Date = {row[1]}\n\n"

    else:
        result = "Incorrect entry. Please enter a number 1-8 to display query results."

    # Close MySQL Connection
    close_connection(cursor, myConnection)
    return result



def insert_exchange(input: str) -> str:
    """
    This method performs an INSERT operation to the ExchangeInfo.Exchange table

    Parameters:
        name:
        address:
        time_zone:
        has_trading_floor:
    """
    name, address, time_zone, has_trading_floor = input.split(',').strip()
    values = (name, address, time_zone, has_trading_floor)

    try:
        myConnection, cursor = create_connection('root', 'cmo5', 'localhost', 'ExchangeInfo')
        insert_exchange_query = """
                                INSERT INTO ExchangeInfo.Exchange(ExchangeName, Address, TimeZone, HasFloor)
                                    VALUES (%s, %s, %s, %s);
                                """
        cursor.execute(insert_exchange_query, values)
        myConnection.commit()
        output = f"Successfully inserted exchange {name}!"
    except Exception as exc:
        output = f"Error inserting Exchange {name}"
        raise Exception(output)
    finally:
        if cursor and myConnection:
            close_connection(cursor, myConnection)

    return output



def insert_asset_class(name: str) -> str:
    """
    This method performs an INSERT operation to the ExchangeInfo.AssetClass table

    Parameters:
        name:
    """
    try:
        myConnection, cursor = create_connection('root', '$A!nts2497', 'localhost', 'ExchangeInfo')   
        values = (name,)
        insert_asset_class_query = """
                                INSERT INTO ExchangeInfo.AssetClass(AssetClassName)
                                    VALUES (%s);
                                """
        cursor.execute(insert_asset_class_query, values)
        myConnection.commit()
        output = f"Succesfully inserted asset class {name}!"
    except Exception as exc:
        output = f"Error adding new AssetClass {name}"
        raise Exception("Error adding new AssetClass")
    finally:
        close_connection(cursor, myConnection)
    
    return output

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Exchange Database Explorer")

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
    )


    # Top Frame - Query Selection
    top_frame = tk.Frame(root, padx=10, pady=10)
    top_frame.pack(fill=tk.X)
    query = tk.Label(top_frame, text=query_list_text, wraplength=400, justify="left")
    query.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
    instruction_label = tk.Label(top_frame, text="Enter a number to run the corresponding query:", justify="left", font=("Arial", 10, "bold"))
    instruction_label.grid(row=1, column=0, sticky="w", pady=5)
    query_input = tk.Entry(top_frame, width=5)
    query_input.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    run_query_button = tk.Button(top_frame, text="Submit", command=lambda: result_label.config(text=run_query(query_input.get())))
    run_query_button.grid(row=1, column=2, sticky="w", padx=5, pady=5)

    # Middle Frame - Display Results
    middle_frame = tk.Frame(root, padx=10, pady=10)
    middle_frame.pack(fill=tk.X)
    result_label = tk.Label(middle_frame, text="", anchor="w", width=60, fg="green")
    result_label.grid(row=0, column=0, sticky="w")

    # Bottom Frame - Insert Statements
    # Insert Asset Class
    bottom_frame = tk.Frame(root, padx=10, pady=10)
    bottom_frame.pack(fill=tk.X)
    asset_class_label = tk.Label(bottom_frame, text="Insert new Asset Class (AssetClassName):", justify="left", font=("Arial", 10, "bold"))
    asset_class_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    asset_class_text_box = tk.Entry(bottom_frame)
    asset_class_text_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    insert_button = tk.Button(bottom_frame, text="Submit", command=lambda: result_label.config(text=insert_asset_class(asset_class_text_box.get())))
    insert_button.grid(row=0, column=2, padx=5, pady=5)
    # Insert Exchange
    exchange_label = tk.Label(bottom_frame, text="Insert new Exchange (ExchangeName,Address,TimeZone,HasPhysicalTradingFloor,TradingHours):", justify="left", font=("Arial", 10, "bold"))
    exchange_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    exchange_text_box = tk.Entry(bottom_frame)
    exchange_text_box.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    insert_exchange_button = tk.Button(bottom_frame, text="Submit", command=lambda: result_label.config(text=insert_exchange(exchange_text_box.get())))
    insert_exchange_button.grid(row=1, column=2, padx=5, pady=5)

    # Run the GUI loop
    root.mainloop()
