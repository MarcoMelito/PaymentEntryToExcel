from file_operation import Operation
#from datetime import datetime, timedelta
import tkinter
import tkinter.messagebox
import customtkinter
from CTkTable import *
from paymentsearcher import PaymentSearcher

# Set appearance and color of the UI
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# Class App that contains all UI settings
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Set a variable for date
        self.current_date = None
        # Set title
        self.title("Payments")
        # Configure window
        self.geometry(f"{1600}x{550}")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=(2, 3), weight=0)

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, height=580, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(index=8, weight=1)

        # Create subtitle label
        self.subtitle_label = customtkinter.CTkLabel(self.sidebar_frame, text="ENTER PAYMENTS\n "
                                                                              "Powered by Marco Melito",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.subtitle_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create Instructions label
        self.instructions_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                     text="Instructions \n\n To begin, set the date.\n "
                                                          "Once the date is set,\n "
                                                          "the button to enter payments will be enabled.\n")
        self.instructions_label.grid(row=1, column=0, padx=(10, 10), pady=(20, 15), sticky="nsew")

        # Create sidebar button set date, insert payments, get daily payments + search, all payments list
        # Set date button, open an input dialog
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="SET DATE",
                                                        command=self.open_input_dialog_event)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=15)
        # Button that allows to view the insertion frame
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="INSERT PAYMENTS",
                                                        command=self.insert_payments_frame)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=15)

        # Button that allow to view daily payments and search button
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="DAILY PAYMENTS + SEARCH",
                                                        command=self.list_payments_frame)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=15)

        # Button that allow to view all payments
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="ALL PAYMENTS VIEW",
                                                        command=self.all_payments_frame)
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=15)

        # Label for appearance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=15, pady=0)
        # Dropdown menu for change appearance mode
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        # Set default values
        # Until the date is entered, the “INSERT PAYMENTS” button will be disabled
        self.sidebar_button_2.configure(state="disabled")
        # Set appearance mode on System
        self.appearance_mode_optionemenu.set("System")

    # Static method for change appearance mode
    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Static method for scaling window
    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Open a dialog event for set date
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Insert date:\nFORMAT: DD/MM/AAAA",
                                              title="SET DATE")
        self.current_date = dialog.get_input()

        # Disable button "SET DATE"
        self.sidebar_button_1.configure(state="disabled")
        # Active button "INSERT PAYMENTS"
        self.sidebar_button_2.configure(state="active")

    # Create frame for insert payments
    def insert_payments_frame(self):
        # Create the insert frame
        self.insert_frame = customtkinter.CTkFrame(master=self, width=1400, height=550, corner_radius=0)
        self.insert_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.insert_frame.grid_columnconfigure(2, weight=2)
        # Create the entry label for the AMOUNT
        self.amount_entry = customtkinter.CTkEntry(self.insert_frame, placeholder_text="AMOUNT")
        self.amount_entry.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create the entry label for the BILL NUMBER
        self.n_bil_entry = customtkinter.CTkEntry(self.insert_frame, placeholder_text="BILL NUMBER")
        self.n_bil_entry.grid(row=2, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create the entry label for the ISSUE DATE
        self.issue_date_entry = customtkinter.CTkEntry(self.insert_frame, placeholder_text="ISSUE DATE")
        # Set the date with date get in self.current_date
        self.issue_date_entry.insert(0, self.current_date)
        self.issue_date_entry.grid(row=3, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create the entry label for the FULL NAME / COMPANY NAME
        self.name_entry = customtkinter.CTkEntry(self.insert_frame,
                                                 placeholder_text="FULL NAME / COMPANY NAME")
        self.name_entry.grid(row=4, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create the entry label for the TRANSACTION CODE
        self.code_entry = customtkinter.CTkEntry(self.insert_frame,
                                                 placeholder_text="TRANSACTION CODE (VALUES AFTER \"UN \")")
        self.code_entry.grid(row=5, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create the entry label for the STORE NAME
        self.store_entry = customtkinter.CTkEntry(self.insert_frame, placeholder_text="STORE NAME")
        self.store_entry.grid(row=6, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create a button "Reset" that call clear_entry method
        self.main_button_1 = customtkinter.CTkButton(self.insert_frame,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Reset",
                                                     command=self.clear_entry)
        self.main_button_1.grid(row=8, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Create a button "Save" that call save method
        self.main_button_2 = customtkinter.CTkButton(self.insert_frame,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Save",
                                                     command=self.save)
        self.main_button_2.grid(row=8, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # Clear the entry and set the placeholder text
    def clear_entry(self):
        self.amount_entry.delete(0, tkinter.END)
        self.amount_entry.configure(placeholder_text="AMOUNT")
        self.n_bil_entry.delete(0, tkinter.END)
        self.n_bil_entry.configure(placeholder_text="BILL NUMBER")
        self.name_entry.delete(0, tkinter.END)
        self.name_entry.configure(placeholder_text="FULL NAME / COMPANY NAME")
        self.code_entry.delete(0, tkinter.END)
        self.code_entry.configure(placeholder_text="TRANSACTION CODE (VALUES AFTER \"UN\")")
        self.store_entry.delete(0, tkinter.END)
        self.store_entry.configure(placeholder_text="STORE NAME")
        # Focus on the amount_entry
        self.amount_entry.focus()

    # Check if there are any errors, if not call operation class for update the Excel file
    def save(self):
        # Save the data entered a variable for each data and format it correctly
        amount = self.amount_entry.get()
        n_bill = self.n_bil_entry.get().upper()
        issue = self.issue_date_entry.get()
        name = self.name_entry.get().upper()
        code = "UN " + self.code_entry.get().upper()
        store = self.store_entry.get().upper()

        # Checks for empty fields, if true it opens an error message window
        if len(amount) == 0 or len(n_bill) == 0 or len(issue) == 0 or len(name) == 0 or len(code) == 0:
            tkinter.messagebox.showinfo(title="Ops!", message="Do not leave blank fields!")
        else:
            # Check if the length of the transaction code
            if len(code) == 11:
                # Check if the length and last letter of bill number
                if len(n_bill) == 11 and (n_bill[-1] == "G" or n_bill[-1] == "E"):
                    # Open an ask ok message box to check the data entered and save the output on is_ok variable
                    is_ok = tkinter.messagebox.askokcancel(title="Payment Data",
                                                           message=f"These are the details entered: \n"
                                                                   f"Amount: {amount.replace(".", ",")}\n"
                                                                   f"Bill number: {n_bill}\n"
                                                                   f"Date issue: {issue}\n"
                                                                   f"Full name: {name}\n"
                                                                   f"Transaction code: {code}\n"
                                                                   f"Store name: {store}\n"
                                                                   f"Is it ok to save?")
                    # If is_ok is true call Operation class
                    if is_ok:
                        operation = Operation()
                        # Call update_file from Operation class, if return true data are correctly saved
                        if operation.update_file(entry=[self.current_date,
                                                 float(amount),
                                                 n_bill,
                                                 issue,
                                                 name,
                                                 code,
                                                 store]):
                            # Opens a message box certifying successful entry
                            tkinter.messagebox.showinfo(message="Successful entry")
                            # Call to clear_entry for reset and get new payment
                            self.clear_entry()
                        else:
                            # Opens a message box for an entry error
                            tkinter.messagebox.showinfo(message="There is an error")
                else:
                    # Opens a message box for an incorrect bill number
                    tkinter.messagebox.showinfo(title="Ops!", message="Incorrect bill number!")
            else:
                # Opens a message box for an incorrect transaction code
                tkinter.messagebox.showinfo(title="Ops!", message="Incorrect transaction code!")

    # Create a frame for get the daily list of payments and search option
    def list_payments_frame(self):
        # Create frame the daily list of payments and search option
        self.payment_frame = customtkinter.CTkScrollableFrame(master=self, width=1400, height=550)
        self.payment_frame.grid(row=0, column=1, sticky="nsew")
        self.payment_frame.grid_columnconfigure(3, weight=1)

        # Create the search button and call search_payments
        self.search_button = customtkinter.CTkButton(self.payment_frame,
                                                     text="SEARCH",
                                                     command=self.search_payments)
        self.search_button.grid(row=0, column=1)

        # Call PaymentSearcher class
        stat = PaymentSearcher()
        date = self.current_date
        # Defines the column headers of the table.
        headers = ["PAYMENT DATE", "AMOUNT", "BILL NUMBER", "ISSUE DATE", "FULL NAME \n COMPANY NAME",
                   "TRANSACTION CODE", "STORE"]
        # Call daily_payments from PaymentSearcher class and get the list of daily payment
        daily_list_payment = stat.daily_payments(date)
        # Initialize or update the table
        self.table = CTkTable(master=self.payment_frame, row=len(daily_list_payment), column=7,
                              values=daily_list_payment)
        # Adds headers as the first row of the table (index 0).
        self.table.add_row(headers, index=0)
        # Adds an index "N" for get the progressive of the list
        index_value = ["N"]
        index_value += [i+1 for i in range(len(daily_list_payment)+1)]
        # Adds the numbering column to the table, at index 8.
        self.table.add_column(index_value, index=8)
        self.table.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        self.table.grid_rowconfigure(0, weight=5)

    # Update the frame list_payments_frame with the result of search
    def search_payments(self):
        # Open a dialog event to get the data to search
        dialog = customtkinter.CTkInputDialog(text="Insert payment information:"
                                                   "\nTRANSACTION CODE "
                                                   "\nFULL NAME / COMPANY NAME",
                                              title="Search")
        info_pagamento = dialog.get_input()
        # Defines the column headers of the table.
        headers = ["PAYMENT DATE", "AMOUNT", "BILL NUMBER", "ISSUE DATE", "FULL NAME \n COMPANY NAME",
                   "TRANSACTION CODE", "STORE"]
        stat = PaymentSearcher()
        # Call search_payments from PaymentSearcher class and get the list payment
        result = stat.search_payments(info_pagamento.upper())
        # Create a frame for search result
        self.search_frame = customtkinter.CTkScrollableFrame(master=self, width=1400, height=550)
        self.search_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        # Check if result is empty
        if len(result) == 0:
            # If is empty create a label that says no result
            self.label = customtkinter.CTkLabel(self.search_frame,
                                                text="The search produced no results.",
                                                anchor="w")
            self.label.grid(row=7, column=0, padx=20, pady=(10, 0))
        else:
            # If is not empty create a table with the result of search
            self.table = CTkTable(master=self.search_frame, row=len(result), column=7, values=result)
            # Adds headers as the first row of the table (index 0).
            self.table.add_row(headers, index=0)
            self.table.grid_rowconfigure(0, weight=2)
            self.table.grid(row=1, column=1, padx=20, pady=20)

    # Create a frame for get a list of all payments
    def all_payments_frame(self):
        # Create the frame
        self.payment_frame = customtkinter.CTkScrollableFrame(master=self, width=1400, height=550)
        self.payment_frame.grid(row=0, column=2, sticky="nsew")
        self.payment_frame.grid_columnconfigure(3, weight=1)

        # Call daily_payments from PaymentSearcher class
        stat = PaymentSearcher()
        # With payments_directory get a list of all_payments
        payments_list = stat.payments_directory()
        # Save the length of the list
        length_list = len(payments_list)
        # Gets the number of pages needed, with a maximum of 50 items per page
        num_option = int(length_list/50)+1
        # Iterate the number of pages for the dropdown combobox
        option_list = []
        for i in range(num_option):
            option_list.append(f"PAGES {i+1}")

        # Handles the selection of a page from the combobox, updating the payment table with the corresponding data
        def combobox_callback(choice):
            # Get the number from choice, example choice = "PAGES 1" -> num_choice = 1
            num_choice = int(choice[6:])
            # Calculates the beginning index for data selection. MAX 50 items
            start_range = (num_choice - 1) * 50
            # Calculates the end index for data selection. MAX 50 items
            end_range = num_choice * 50
            # Extracts the subset of data from payments_list. This represents the current page of payments displayed.
            result = payments_list[start_range:end_range]
            # Defines the column headers of the table.
            headers = ["PAYMENT DATE", "AMOUNT", "BILL NUMBER", "ISSUE DATE", "FULL NAME \n COMPANY NAME",
                       "TRANSACTION CODE", "STORE"]
            # Initialize or update the table
            self.table = CTkTable(master=self.payment_frame, row=len(result), column=7, values=result)
            # Adds headers as the first row of the table (index 0).
            self.table.add_row(headers, index=0)
            # Adds an index "N" for get the progressive of the list
            index_value = ["N"]
            index_value += [i + 1 for i in range(len(payments_list) + 1)]
            # Adds the numbering column to the table, at index 8.
            self.table.add_column(index_value, index=8)
            self.table.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)
            self.table.grid_rowconfigure(0, weight=5)

        # Initialize a new combobox
        self.combobox = customtkinter.CTkComboBox(master=self.sidebar_frame, values=option_list,
                                                  command=combobox_callback)
        # Sets the default text displayed in the combobox when a selection has not yet been made or to guide the user.
        self.combobox.set("SELECT PAGE")
        self.combobox.grid(row=8, column=0, padx=20, pady=15)
