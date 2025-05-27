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

def run_query_one():
    """
    This method runs the first query in the list
    """
    myConnection, cursor = create_connection('root', 'cmo5', 'localhost', 'ExchangeInfo')

    # Run Query and display results
    query = """
            SELECT * FROM ExchangeInfo.Holiday
            LIMIT 10;
            """
    cursor.execute(query)
    query_results = cursor.fetchall()

    for row in query_results:
        print(f"firstName = {row[0]}")
        print(f"lastName = {row[1]}")
        print(f"email = {row[2]}")
    print("\n")

    close_connection(cursor, myConnection)

def insert_exchange(name: str, address: str, time_zone: str, has_trading_floor: bool) -> None:
    """
    This method performs an INSERT operation to the ExchangeInfo.Exchange table

    Parameters:
        name:
        address:
        time_zone:
        has_trading_floor:
    """

    myConnection, cursor = create_connection('root', 'cmo5', 'localhost', 'ExchangeInfo')
    values = (name, address, time_zone, has_trading_floor)
    insert_exchange_query = """
                            INSERT INTO ExchangeInfo.Exchange(ExchangeId, ExchangeName, Address, TimeZone, HasFloor)
                                VALUES (%s, %s, %s, %s, %s);
                            """
    cursor.execute(insert_exchange_query, values)
    myConnection.commit()
    close_connection(cursor, myConnection)

def insert_asset_class(name: str) -> None:
    """
    This method performs an INSERT operation to the ExchangeInfo.AssetClass table

    Parameters:
        name:
    """

    myConnection, cursor = create_connection('root', 'cmo5', 'localhost', 'ExchangeInfo')   
    values = (name)
    insert_asset_class_query = """
                            INSERT INTO ExchangeInfo.AssetClass(AssetClassId, AssetClassName)
                                VALUES (%s, %s);
                            """
    cursor.execute(insert_asset_class_query, values)
    myConnection.commit()
    close_connection(cursor, myConnection)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Exchange Database Explorer")

    query_list_text = (
        "Query List\n\n"
        "1. Display the number of symbols listed on CME exchange that are a future but not an option.\n"
        "2. Display all exchanges that have AAPL listed but don’t have ZBRA listed.\n"
        "3. Display unique symbols for each contract type that trade at the CME\n"
        "4. Display all exchanges that are subject to SEC regulations and have TRIP listed\n"
        "5. Display all exchange names located in either Chicago and New York\n"
        "6. How many products are only listed on one exchange?\n"
        "7. Which CME products are closed on Christmas and New Year’s Day?\n"
        "8. What are the listed trading hours for each exchange on all holidays?\n"
        "9. Which Broker-Dealers are not members of NYSE?\n"
        "10. What non-weekend off days do Broker-Dealers have?"   
    )

    # Top Frame - Query Selection
    top_frame = tk.Frame(root, padx=10, pady=10)
    top_frame.pack(fill=tk.X)
    query_1 = tk.Label(top_frame, text=query_list_text, wraplength=400, justify="left")
    query_1.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
    instruction_label = tk.Label(top_frame, text="Enter a number to run the corresponding query:", justify="left")
    instruction_label.grid(row=1, column=0, sticky="w", pady=5)
    query_input = tk.Entry(top_frame, width=5)
    query_input.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    # Set the submit_button command to this commented line for result
    # command=lambda: run_query(int(entry.get()) - 1)
    run_query_button = tk.Button(top_frame, text="Submit")
    run_query_button.grid(row=1, column=2, sticky="w", padx=5, pady=5)

    # Middle Frame - Insert Statements
    # Insert Asset Class
    middle_frame = tk.Frame(root, padx=10, pady=10)
    middle_frame.pack(fill=tk.X)
    asset_class_label = tk.Label(middle_frame, text="Insert new Asset Class (AssetClassName):")
    asset_class_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    asset_class_text_box = tk.Entry(middle_frame)
    asset_class_text_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    insert_button = tk.Button(middle_frame, text="Submit")
    insert_button.grid(row=0, column=2, padx=5, pady=5)
    # Insert Exchange
    exchange_label = tk.Label(middle_frame, text="Insert new Exchange Info (ExchangeName,Address,TimeZone,HasPhysicalTradingFloor):")
    exchange_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    exchange_text_box = tk.Entry(middle_frame)
    exchange_text_box.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    insert_exchange_button = tk.Button(middle_frame, text="Submit")
    insert_exchange_button.grid(row=1, column=2, padx=5, pady=5)

    # Bottom Frame - Display Results
    bottom_frame = tk.Frame(root, padx=10, pady=10)
    bottom_frame.pack(fill=tk.X)
    result_label = tk.Label(bottom_frame, text="", anchor="w", width=60)
    result_label.grid(row=0, column=0, sticky="w")
    exit_button = tk.Button(bottom_frame, text="Exit", command=root.quit)
    exit_button.grid(row=0, column=1, sticky="e", padx=5)

    # Run the GUI loop
    root.mainloop()
