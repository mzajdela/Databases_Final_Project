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

def run_query(numQuery: int):
    """
    This method runs the first query in the list
    """
    myConnection, cursor = create_connection('root', 'cmo5', 'localhost', 'ExchangeInfo')

    # Run Query and display results
    numQuery = int(numQuery)
    result = ""

    if numQuery == 1:
        query = """
                SELECT * FROM ExchangeInfo.Holiday
                LIMIT 5;
                """
        cursor.execute(query)
        query_results = cursor.fetchall()

        for row in query_results:
            result += f"Holiday Id = {row[0]}\n"
            result += f"Holiday Name = {row[1]}\n"
            result += f"Is Early Close = {row[2]}\n"
            result += f"Holiday Date = {row[3]}\n"
            result += f"Calendar Year = {row[4]}\n"
            result += "\n"
    else:
        result = "Incorrect entry. Please enter a number 1-10 to display query results."

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
        output = f"Succesfully inserted exchange {name}!"
    except Exception as exc:
        output = f"Error inserting Exchange {name}"
        raise Exception("Error inserting Exchange")
    finally:
        close_connection(cursor, myConnection)
    
    return output

def insert_asset_class(name: str) -> str:
    """
    This method performs an INSERT operation to the ExchangeInfo.AssetClass table

    Parameters:
        name:
    """
    try:
        myConnection, cursor = create_connection('root', 'cmo5', 'localhost', 'ExchangeInfo')   
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
    query = tk.Label(top_frame, text=query_list_text, wraplength=400, justify="left")
    query.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
    instruction_label = tk.Label(top_frame, text="Enter a number to run the corresponding query:", justify="left")
    instruction_label.grid(row=1, column=0, sticky="w", pady=5)
    query_input = tk.Entry(top_frame, width=5)
    query_input.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    # Set the submit_button command to this commented line for result
    # command=lambda: run_query(int(entry.get()) - 1)
    run_query_button = tk.Button(top_frame, text="Submit", command=lambda: result_label.config(text=run_query(query_input.get())))
    run_query_button.grid(row=1, column=2, sticky="w", padx=5, pady=5)

    # Middle Frame - Display Results
    middle_frame = tk.Frame(root, padx=10, pady=10)
    middle_frame.pack(fill=tk.X)
    result_label = tk.Label(middle_frame, text="", anchor="w", width=60)
    result_label.grid(row=0, column=0, sticky="w")

    # Bottom Frame - Insert Statements
    # Insert Asset Class
    bottom_frame = tk.Frame(root, padx=10, pady=10)
    bottom_frame.pack(fill=tk.X)
    asset_class_label = tk.Label(bottom_frame, text="Insert new Asset Class (AssetClassName):")
    asset_class_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    asset_class_text_box = tk.Entry(bottom_frame)
    asset_class_text_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    insert_button = tk.Button(bottom_frame, text="Submit", command=lambda: result_label.config(text=insert_asset_class(asset_class_text_box.get())))
    insert_button.grid(row=0, column=2, padx=5, pady=5)
    # Insert Exchange
    exchange_label = tk.Label(bottom_frame, text="Insert new Exchange Info (ExchangeName,Address,TimeZone,HasPhysicalTradingFloor):")
    exchange_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    exchange_text_box = tk.Entry(bottom_frame)
    exchange_text_box.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    insert_exchange_button = tk.Button(bottom_frame, text="Submit", command=lambda: result_label.config(text=insert_exchange(exchange_text_box.get())))
    insert_exchange_button.grid(row=1, column=2, padx=5, pady=5)

    # Run the GUI loop
    root.mainloop()
