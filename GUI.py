import tkinter as tk

QUERY_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

def run_query(num_query: int):
    # Create MySQL connection
    myConnection = mysql.connector.connect(user='root', password='cmo5', host='localHost', database='myExchange')
    cursor = myConnection.cursor()

    # Run Query and display results
    query = QUERY_LIST[num_query]
    cursor.execute(query)
    query_results = cursor.fetchall()
    for row in query_results:
        print(f"firstName = {row[0]}")
        print(f"lastName = {row[1]}")
        print(f"email = {row[2]}")
    print("\n")

    # Close MySQL Connection
    cursor.close()
    myConnection.close()

def test_print():
    result_label.config(text="Casey\nCasey\nCasey")

# Create the main window
root = tk.Tk()
root.title("Exchange Database Explorer")
root.geometry("400x300")

# Create widgets
label = tk.Label(root, text="Choose a number to run the corresponding query", wraplength=350)
query_1 = tk.Label(root, text="1. Display all exchanges in Chicago/nTesting", wraplength=350)
text_box = tk.Text(root, height=1, width=5)
# Set the submit_button command to this commented line for result
# command=lambda: run_query(int(entry.get()) - 1)
submit_button = tk.Button(root, text="Submit", command=test_print)
result_label = tk.Label(root, text="")
exit_button = tk.Button(root, text="Exit", command=root.quit)

# Layout
label.pack(pady=10)
query_1.pack(pady=10)
text_box.pack()
submit_button.pack(pady=5)
result_label.pack()
exit_button.pack()

# Run the GUI loop
root.mainloop()
