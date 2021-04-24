# Import packages
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import csv
import pandas as pd

# Set up Root Window
root = Tk()
root.title("Drills N Bits Stock Tracker")
root.iconbitmap('drillsIcon.ico')
root.resizable(False, False)

# Displays logo in top right
logo = Image.open("drillsLogo.png")
resizedLogo = logo.resize((93, 75), Image.ANTIALIAS)
newLogo = ImageTk.PhotoImage(resizedLogo)
logoLabel = Label(root, image=newLogo)
logoLabel.grid(pady=20, padx=20)

# Displays Title
titleLabel = Label(root, text="Drills N Bits Stock Tracker")
titleLabel.config(font=("Arial", 30))
titleLabel.grid(row=0, column=1, columnspan=4)


# Function containing the "new product window" and any widgets/functions found in it
def open_new_product_win():

    # sets up new product window
    new_product_win = Toplevel(pady=20, padx=20)
    new_product_win.title("Drills N Bits Stock Tracker - Add New")
    new_product_win.iconbitmap('drillsIcon.ico')
    new_product_win.resizable(False, False)

    # Sets up the widgets contained within the window
    new_logoLabel = Label(new_product_win, image=newLogo)
    new_logoLabel.grid()

    new_title_label = Label(new_product_win, text="Add New Product", font=("Arial", 30), padx=20).grid(row=0, column=1, columnspan=2)

    new_id_label = Label(new_product_win, text="ID: ", font=("Arial", 13), pady=10)
    new_id_label.grid(row=1, column=1, sticky=W, columnspan=2)
    new_id_entry = Entry(new_product_win)
    new_id_entry.grid(row=1, column=2, sticky=W)

    new_name_label = Label(new_product_win, text="Name: ", font=("Arial", 13), pady=10)
    new_name_label.grid(row=2, column=1, sticky=W, columnspan=2)
    new_name_entry = Entry(new_product_win)
    new_name_entry.grid(row=2, column=2, sticky=W)

    new_dep_label = Label(new_product_win, text="Department: ", font=("Arial", 13), pady=10)
    new_dep_label.grid(row=3, column=1, sticky=W, columnspan=2)
    new_dep_entry = Entry(new_product_win)
    new_dep_entry.grid(row=3, column=2, sticky=W)

    new_loc_label = Label(new_product_win, text="Location: ", font=("Arial", 13), pady=10)
    new_loc_label.grid(row=4, column=1, sticky=W, columnspan=2)
    new_loc_entry = Entry(new_product_win)
    new_loc_entry.grid(row=4, column=2, sticky=W)

    new_quantity_label = Label(new_product_win, text="Quantity: ", font=("Arial", 13), pady=10)
    new_quantity_label.grid(row=5, column=1, sticky=W, columnspan=2)
    new_quantity_entry = Entry(new_product_win)
    new_quantity_entry.grid(row=5, column=2, sticky=W)

    # function used to clear all boxes in the new product window
    def clear_boxes():
        new_id_entry.delete(0, "end")
        new_name_entry.delete(0, "end")
        new_dep_entry.delete(0, "end")
        new_loc_entry.delete(0, "end")
        new_quantity_entry.delete(0, "end")

    # function to display a message when a new product is added
    def popup():
        messagebox.showinfo("New Product Successfully Added", "New Product Successfully Added")

    # function to append the new product to the end of the CSV file
    def append_data():
        df = pd.read_csv("csvFiles/drills.csv")

        new_record = {'ID': new_id_entry.get(),
                      'name': new_name_entry.get(),
                      'department': new_dep_entry.get(),
                      'location': new_loc_entry.get(),
                      'quantity': new_quantity_entry.get()
                      }

        df2 = pd.DataFrame(new_record, index=[0])

        df3 = df.append(df2, ignore_index=True)

        df3.to_csv("csvFiles/drills.csv", index=False)

        popup()
        clear_boxes()

    # Function to check if any boxes are blank, if so, will return false
    def check_boxes():

        boxes = [new_id_entry, new_name_entry, new_dep_entry, new_loc_entry, new_quantity_entry]
        check = True

        for box in boxes:
            if box.get() == "":
                check = False

        return check

    blank_warning = Label(new_product_win, text="One or more boxes are blank, please complete all boxes", font=("Arial", 13), pady=10, fg="red" )

    # Function to run the append process or display message if any boxes are blank
    def run_append():

        if check_boxes() is False:
            blank_warning.grid(row=6, columnspan=3)
        else:
            append_data()

    new_button = Button(new_product_win, text="Add New Product", padx=20, pady=10, bg="blue", fg="white", command=run_append).grid(row=7, columnspan=3)


# Displays New Product Button
newProductButton = Button(root, text="New Product", command=open_new_product_win)
newProductButton.config(height=5, width=15, bg="blue", fg="white")
newProductButton.grid(row=0, column=5, padx=20)

# Displays search box and label
searchBoxLabel = Label(root, text="Product ID: ")
searchBoxLabel.config(font=("Arial", 15), width=13)
searchBoxLabel.grid(row=1, column=2, padx=20, pady=50, sticky=E)

searchBox = Entry(root)
searchBox.grid(row=1, column=3, padx=20, pady=50, sticky=W)

# Display "Search By" label and box + logic for the dropdown
searchByLabel = Label(root, text="Search By: ")
searchByLabel.config(font=("Arial", 15))
searchByLabel.grid(row=1, padx=20, pady=50)


# function to change the text of the "search by" label to display which type of search you ar doing (either ID or Name)
def combo_click(event):
    searchBoxLabel.config(text=searchByDropdown.get() + ": ")


# sets up the "search by" dropdown
searchOptions = ["Product ID", "Product Name"]
searchByDropdown = ttk.Combobox(root, value=searchOptions)
searchByDropdown.current(0)
searchByDropdown.bind("<<ComboboxSelected>>", combo_click)
searchByDropdown.grid(row=1, column=1, sticky=W)

# Sets up a results frame
results_frame = Frame(root)


# Function defining the logic of searching, as well as containing functions to add/take away stock
def search(value, type_p):

    # loops through widgets in the results frame and removes them with each search
    for widget in results_frame.winfo_children():
        widget.destroy()

    # Sets the CSV file location
    filename = 'csvFiles/drills.csv'

    # opens the CSV file and sets up a reader
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        search_type = type_p
        search_value = value

        # searches through the CSV file for the search value, if it finds it, returns the line, otherwise remains None
        def search_algorithm(type_s):
            for line in csv_reader:
                if value == line[type_s]:
                    return line

        # runs the search using the selected search type
        # search type is found using a helper function get_type() (found below @ approx line 280)
        search_result = search_algorithm(search_type)

        # if/elif/else statement - checks if the search could be found, if it can, displays the results and allows for
        # adding/subtracting stock. if the result cannot be found or the box was blank, displays another message
        if search_result is not None:

            # displays results frame and labels with product details
            results_frame.grid(row=2, columnspan=6, pady=(0, 30))

            product_id_label = Label(results_frame, text="Product ID: " + search_result['ID'], font=("Arial", 13), pady=10)
            product_id_label.grid()
            product_name_label = Label(results_frame, text="Product Name: " + search_result['name'], font=("Arial", 13), pady=10)
            product_name_label.grid(row=1)
            product_dep_label = Label(results_frame, text="Product Department: " + search_result['department'], font=("Arial", 13), pady=10)
            product_dep_label.grid(row=2)
            product_loc_label = Label(results_frame, text="Product Location: " + search_result['location'], font=("Arial", 13), pady=10)
            product_loc_label.grid(row=3)
            product_quantity_label = Label(results_frame, text="Product Quantity: " + search_result['quantity'], font=("Arial", 13), pady=10)
            product_quantity_label.grid(row=4)
            checkout_label = Label(results_frame, text="Quantity to Check In / Out:", font=("Arial", 13), pady=10)
            checkout_label.grid(row=5)
            checkout_entry = Entry(results_frame)
            checkout_entry.grid(row=6)

            # Displays warning if quantity box is blank

            blank_warning = Label(results_frame, text="Checkout box blank", font=("Arial", 13), pady=5, fg="red")

            def blank_box():

                if checkout_entry.get() == "":
                    blank_warning.grid(row=7)
                else:
                    blank_warning.grid_forget()

            # Logic for adding quantity

            def add_q(type1, value1):

                if type1 == 'ID':
                    value1 = int(value1)

                if checkout_entry.get() == "":
                    blank_box()
                else:
                    blank_box()
                    df = pd.read_csv("csvFiles/drills.csv")
                    index = df[df[type1] == value1].index.values
                    df.loc[index, ['quantity']] = df.loc[index, ['quantity']] + int(checkout_entry.get())
                    df['ID'] = df['ID'].astype(int)
                    df['quantity'] = df['quantity'].astype(int)
                    df.to_csv("csvFiles/drills.csv", index=False)
                    new_quantity = df[df[type1] == value1].values[0]
                    product_quantity_label.config(text="Product Quantity: " + str(new_quantity[4]))

            # Logic for taking away quantity

            def minus_q(type1, value1):

                if type1 == 'ID':
                    value1 = int(value1)

                if checkout_entry.get() == "":
                    blank_box()
                else:
                    blank_box()
                    df = pd.read_csv("csvFiles/drills.csv")
                    index = df[df[type1] == value1].index.values
                    df.loc[index, ['quantity']] = df.loc[index, ['quantity']] - int(checkout_entry.get())
                    df['ID'] = df['ID'].astype(int)
                    df['quantity'] = df['quantity'].astype(int)
                    df.to_csv("csvFiles/drills.csv", index=False)
                    new_quantity = df[df[type1] == value1].values[0]
                    product_quantity_label.config(text="Product Quantity: " + str(new_quantity[4]))

            checkout_add = Button(results_frame, text="+", bg="blue", fg="white", width=5, command=lambda: add_q(search_type, search_value))
            checkout_add.grid(row=6, column=1, sticky=W)
            checkout_minus = Button(results_frame, text="-", bg="blue", fg="white", width=5, command=lambda: minus_q(search_type, search_value))
            checkout_minus.grid(row=6, column=2, sticky=W)

        elif search_value == "":

            results_frame.grid(row=2, columnspan=6)

            blank_result_label = Label(results_frame, text="Search was blank", font=("Arial", 13), pady=20, fg="red")
            blank_result_label.grid()

        else:

            results_frame.grid(row=2, columnspan=6)

            no_result_label = Label(results_frame, text="No result found for \"" + search_value + "\"", font=("Arial", 13), pady=20, fg="red")
            no_result_label.grid()


# Function to run the search when the button is pressed
def run_search():

    def get_type():
        if searchByDropdown.get() == "Product ID":
            return 'ID'
        elif searchByDropdown.get() == "Product Name":
            return 'name'

    search(searchBox.get(), get_type())


# Allows for pressing enter to search
def enter_search(event):
    run_search()


root.bind('<Return>', enter_search)


# function to clear the search boxes when the search button is pressed
def clear_search():
    results_frame.grid_forget()
    searchBox.delete(0, "end")


# Display search button
searchButton = Button(root, text="Search", command=run_search)
searchButton.config(height=2, width=15, bg="blue", fg="white")
searchButton.grid(row=1, column=4)

# Display clear button
clearButton = Button(root, text="Clear")
clearButton.config(height=2, width=15, bg="blue", fg="white", command=clear_search)
clearButton.grid(row=1, column=5)

# Loop to keep the window open until closed
root.mainloop()
