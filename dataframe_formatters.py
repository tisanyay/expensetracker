import re
import pandas as pd
import io

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
    
def append_transaction_history(file, transaction_history):

    cleaned_csv = ""

    with open(file, 'r') as file:
        for line in file:
            valid = check_if_line_is_valid(line)

            if valid:
                cleaned_csv += valid
                cleaned_csv += "\n"

    df = pd.read_csv(io.StringIO(cleaned_csv))
    return pd.concat([transaction_history, df]).drop_duplicates()

def append_uploaded_file_transaction_history(file, transaction_history):
    cleaned_csv = ""
    stringio = io.StringIO(file.getvalue().decode("utf-8"))
    for line in stringio:
        valid = check_if_line_is_valid(line)

        if valid:
            cleaned_csv += valid
            cleaned_csv += "\n"
    df = pd.read_csv(io.StringIO(cleaned_csv))
    return pd.concat([transaction_history, df]).drop_duplicates()