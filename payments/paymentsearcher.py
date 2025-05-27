import pandas as pd


# I created this class to perform the search a payments and get the list of payments entered
class PaymentSearcher:
    def __init__(self):
        # File path for the Excel file containing all payments
        self.file_path = "all_payments./PAYMENTS_FILE.xlsx"

    # Open the Excel file and return the sheet
    def open_file(self):
        with pd.ExcelFile(self.file_path) as xls:
            payments_file = pd.read_excel(xls, "Foglio1")

        return payments_file

    # Get all daily payments and return it as a list
    def daily_payments(self, data):
        payments_df = self.open_file()
        payments = payments_df.loc[payments_df["PAYMENT DATE"] == data]
        payments_list = self.get_list_payments(payments)
        return payments_list

    # Search for a specific payment or the payments of a specific user
    def search_payments(self, info_payments):
        payments_df = self.open_file()

        # Check the length of info_payments
        if len(info_payments) == 11:
            # If it starts with ‘UN’ the search will be for the transition code
            if info_payments[0:2] == "UN":
                payments = payments_df.loc[payments_df["TRANSACTION CODE"] == info_payments]
                payments_list = self.get_list_payments(payments)
                return payments_list
            # If it ends with ‘G’ or 'E' the search will be for the bills number
            elif info_payments[-1] == "G" or "E":
                payments = payments_df.loc[payments_df["BILL NUMBER"] == info_payments]
                payments_list = self.get_list_payments(payments)
                return payments_list
        else:
            # The search will be by costumer name
            payments = payments_df.loc[payments_df["FULL NAME"] == info_payments]
            payments_list = self.get_list_payments(payments)
            return payments_list

    # Get a directory of payments
    def payments_directory(self):
        # Upload payment data
        payments_df = self.open_file()
        # Sort payments by name and date, then group them (uses a lambda function)
        payments = payments_df.sort_values(["FULL NAME", "PAYMENT DATE"]).groupby(["FULL NAME"]).apply(lambda a: a)
        # Converts the resulting object to a Python list
        payments_list = self.get_list_payments(payments)
        # Returns the list of payments
        return payments_list

    # Iterate the payments and append it in a list
    @staticmethod
    def get_list_payments(payments):
        # Initializes an empty list that will contain payments
        list_payments = []
        # Itera on each individual payment within the 'payments.values' collection.
        for payment in payments.values:
            # Adds the current payment to the list.
            list_payments.append(payment)
        # Returns the list of payments
        return list_payments
