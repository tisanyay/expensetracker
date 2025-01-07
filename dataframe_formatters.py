<<<<<<< HEAD
import re
import pandas as pd
import numpy as np
import io

def output_csv(df, directory):
    df.to_csv(directory, index=False)

def remove_special_characters(string):
    return "".join(e for e in string.lower() if e.isalnum())

def check_if_string_in_list(original_string, reference_list):
    if not isinstance(original_string, str):
        return False
    original_list = [remove_special_characters(s) for s in re.split("\\s+|\.|\@|\*|\/|\_|\-", original_string)]
    return any([x in reference_list for x in original_list])

def categorize_vendors(original_string, reference_dict):
    if not isinstance(original_string, str):
        return "Others"
    original_list = [remove_special_characters(s) for s in re.split("\\s+|\.|\@|\*|\/|\_|\-", original_string)]
    for x in original_list:
        for key, value in reference_dict.items():
            if x in value:
                return key
    return "Shopping"

def get_shopping_and_fb_categories(df):
    return df[(df["Debit Amount"].notna()) & (df["Category"].isin(["Shopping", "F&B"]))]

def check_if_line_is_valid(line):
    line = line.strip()
    comma_count = line.count(',')

    if comma_count == 1 or comma_count > 8:
        return 
    
    if comma_count == 6:
        return line

    surplus_commas = comma_count - 6
    line = line[:-surplus_commas]

    if line.count(',') == 6:
        return line
    
def clean_uploaded_file(file):
    cleaned_csv = ""
    stringio = io.StringIO(file.getvalue().decode("utf-8"))
    for line in stringio:
        valid = check_if_line_is_valid(line)

        if valid:
            cleaned_csv += valid
            cleaned_csv += "\n"

    df = pd.read_csv(io.StringIO(cleaned_csv))
    df = clean_transaction_history(df)

    return df

def clean_transaction_history(transaction_history):
    transaction_history["Transaction Date"] = pd.to_datetime(transaction_history["Transaction Date"])
    transaction_history["Debit Amount"] = transaction_history["Debit Amount"].replace({' ': np.nan})
    transaction_history["Debit Amount"] = transaction_history["Debit Amount"].astype(float)
    transaction_history["Credit Amount"] = transaction_history["Credit Amount"].replace({' ': np.nan})
    transaction_history["Credit Amount"] = transaction_history["Credit Amount"].astype(float)
    transaction_history["Date"] = transaction_history["Transaction Date"].dt.strftime('%b %d')
    transaction_history["Month"] = transaction_history["Transaction Date"].dt.strftime('%m %b')
    transaction_history["Transaction Ref1"] = transaction_history["Transaction Ref1"].fillna("")
    transaction_history["Transaction Ref2"] = transaction_history["Transaction Ref2"].fillna("")
    transaction_history["Transaction Ref3"] = transaction_history["Transaction Ref3"].fillna("")
    transaction_history["Vendor"] = transaction_history["Transaction Ref1"] + ' ' + transaction_history["Transaction Ref2"] + ' ' + transaction_history["Transaction Ref3"]
    transaction_history = transaction_history[transaction_history["Reference"] != "ITR"]

    # F&B vendors list
    with open("./restaurants.txt") as restaurants:
        lines = restaurants.readlines()

        restaurant_list = []
        for line in lines:
            line = [remove_special_characters(e) for e in line.split(", ")]
            restaurant_list.extend(line)

        restaurant_list = list(set(restaurant_list))

    # Transport, transfers, salary, and medical lists
    transport_list = ["bus", "grab"]
    transfer_list = ["kwynnzie"]
    salary_list = ["mindef", "saf", "gov"]
    medical_list = ["polyclinic", "clinic"]

    # Vendor group dictionary
    vendor_groups = {
        "F&B": restaurant_list,
        "Transport": transport_list,
        "Transfers": transfer_list,
        "Salary": salary_list,
        "Medical": medical_list
    }

    # Transportation vendors list
    transaction_history["Category"] = transaction_history["Vendor"].apply(lambda x: categorize_vendors(x, vendor_groups))

    return transaction_history

if __name__ == "__main__":
    cleaned_history = "./transaction_history_csv/cleaned_transaction_history.csv"
    addon_history = "./transaction_history_csv/sep-dec.csv"

    transaction_history = pd.read_csv(cleaned_history)
=======
import re
import pandas as pd
import numpy as np
import io

def output_csv(df, directory):
    df.to_csv(directory, index=False)

def remove_special_characters(string):
    return "".join(e for e in string.lower() if e.isalnum())

def check_if_string_in_list(original_string, reference_list):
    if not isinstance(original_string, str):
        return False
    original_list = [remove_special_characters(s) for s in re.split("\\s+|\.|\@|\*|\/|\_|\-", original_string)]
    return any([x in reference_list for x in original_list])

def categorize_vendors(original_string, reference_dict):
    if not isinstance(original_string, str):
        return "Others"
    original_list = [remove_special_characters(s) for s in re.split("\\s+|\.|\@|\*|\/|\_|\-", original_string)]
    for x in original_list:
        for key, value in reference_dict.items():
            if x in value:
                return key
    return "Shopping"

def get_shopping_and_fb_categories(df):
    return df[(df["Debit Amount"].notna()) & (df["Category"].isin(["Shopping", "F&B"]))]

def check_if_line_is_valid(line):
    line = line.strip()
    comma_count = line.count(',')

    if comma_count == 1 or comma_count > 8:
        return 
    
    if comma_count == 6:
        return line

    surplus_commas = comma_count - 6
    line = line[:-surplus_commas]

    if line.count(',') == 6:
        return line
    
def clean_uploaded_file(file):
    cleaned_csv = ""
    stringio = io.StringIO(file.getvalue().decode("utf-8"))
    for line in stringio:
        valid = check_if_line_is_valid(line)

        if valid:
            cleaned_csv += valid
            cleaned_csv += "\n"

    df = pd.read_csv(io.StringIO(cleaned_csv))
    df = clean_transaction_history(df)

    return df

def clean_transaction_history(transaction_history):
    transaction_history["Transaction Date"] = pd.to_datetime(transaction_history["Transaction Date"])
    transaction_history["Debit Amount"] = transaction_history["Debit Amount"].replace({' ': np.nan})
    transaction_history["Debit Amount"] = transaction_history["Debit Amount"].astype(float)
    transaction_history["Credit Amount"] = transaction_history["Credit Amount"].replace({' ': np.nan})
    transaction_history["Credit Amount"] = transaction_history["Credit Amount"].astype(float)
    transaction_history["Date"] = transaction_history["Transaction Date"].dt.strftime('%b %d')
    transaction_history["Month"] = transaction_history["Transaction Date"].dt.strftime('%m %b')
    transaction_history["Transaction Ref1"] = transaction_history["Transaction Ref1"].fillna("")
    transaction_history["Transaction Ref2"] = transaction_history["Transaction Ref2"].fillna("")
    transaction_history["Transaction Ref3"] = transaction_history["Transaction Ref3"].fillna("")
    transaction_history["Vendor"] = transaction_history["Transaction Ref1"] + ' ' + transaction_history["Transaction Ref2"] + ' ' + transaction_history["Transaction Ref3"]
    transaction_history = transaction_history[transaction_history["Reference"] != "ITR"]

    # F&B vendors list
    with open("./restaurants.txt") as restaurants:
        lines = restaurants.readlines()

        restaurant_list = []
        for line in lines:
            line = [remove_special_characters(e) for e in line.split(", ")]
            restaurant_list.extend(line)

        restaurant_list = list(set(restaurant_list))

    # Transport, transfers, salary, and medical lists
    transport_list = ["bus", "grab"]
    transfer_list = ["kwynnzie"]
    salary_list = ["mindef", "saf", "gov"]
    medical_list = ["polyclinic", "clinic"]

    # Vendor group dictionary
    vendor_groups = {
        "F&B": restaurant_list,
        "Transport": transport_list,
        "Transfers": transfer_list,
        "Salary": salary_list,
        "Medical": medical_list
    }

    # Transportation vendors list
    transaction_history["Category"] = transaction_history["Vendor"].apply(lambda x: categorize_vendors(x, vendor_groups))

    return transaction_history

def append_transaction_history(file, transaction_history):
    cleaned_csv = read_transaction_history(file)

    df = pd.read_csv(io.StringIO(cleaned_csv))
    return pd.concat([transaction_history, df]).drop_duplicates()

def read_transaction_history(file):
    cleaned_csv = ""

    for line in file:
        valid = check_if_line_is_valid(line)

        if valid:
            cleaned_csv += valid
            cleaned_csv += "\n"

    return pd.read_csv(io.StringIO(cleaned_csv))

def join_date(df, transaction_history, date):
    df_on_date = df[df["Transaction Date"] == date]
    transaction_on_date = transaction_history[transaction_history["Transaction Date"] == date]

    return pd.concat([df_on_date, transaction_on_date]).drop_duplicates()

def append_uploaded_transaction_history(file, transaction_history):
    df = read_transaction_history(file)    
    df = clean_transaction_history(df)

    if transaction_history.shape[0] == 0:
        return df

    earliest_date = min(transaction_history["Transaction Date"])
    latest_date = max(transaction_history["Transaction Date"])

    df = df[(df["Transaction Date"] < earliest_date) | (df["Transaction Date"] > latest_date)]
    transaction_history_1 = transaction_history[(transaction_history["Transaction Date"] > earliest_date) & (transaction_history["Transaction Date"] < latest_date)]

    join_earlier_history = join_date(df, transaction_history, earliest_date)
    join_later_history = join_date(df, transaction_history, latest_date)

    return pd.concat([join_earlier_history, transaction_history_1, join_later_history, df]) 
 
if __name__ == "__main__":
    cleaned_history = "./transaction_history_csv/cleaned_transaction_history.csv"
    addon_history = "./transaction_history_csv/sep-dec.csv"

    transaction_history = pd.read_csv(cleaned_history)
 
>>>>>>> 220a4fd1450e80cfbe0c4a3f111e8f9f09a9638b
