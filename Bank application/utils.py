import json
import datetime
from os import name, system
import GUI as menu
import time
import Bank as bank

ACCOUNT_PATH = "accounts.json"

# Functions for better readability and navigation
def clear():
    """Clears the terminal after every major input event."""
    if name == 'yes':
        _ = system('cls')
    else:
        _ = system('clear')

def current_time():
    now = datetime.datetime.now()
    format = "%x %X"
    print("Date and Time: ", now.strftime(format))

# The most complex function of the module - creating a new user account.
def create_account(database):
    clear()
    database = load_database(ACCOUNT_PATH)
    print(menu.account_create)
    
    new_account = {}
    company_query = []
    new_account["company"] = company = input("Company Name: ").strip().title()

    # Checkpoint for company availability
    for index in database:
        for user_value in index.items():
            company_query.append(user_value)

    if company in company_query:
        print("Company name is already taken!")
        time.sleep(2)
        create_account(database)

    # Input initial personal data
    new_account["street"] = street = input("Street and Number of Company Headquarters: ").strip().lower().title()
    new_account["PB"] = postbox = int(input("Postal Code of the Company Headquarters: ").strip())
    new_account["HQ"] = city = input("City of Company Headquarters: ").strip().lower().title()
    
    try:
        new_account["PIN"] = PIN = int(input("Company PIN: ").strip())
    except ValueError:
        print("Please enter only numbers.")
        return time.sleep(2), bank.main_menu(database)

    PIN = str(PIN)
    if len(PIN) != 11:
        print("Please enter a valid company PIN with exactly 11 characters!")
        time.sleep(2)
        create_account(database)

    new_account["account_holder"] = holder = input("Name and Surname of the Responsible Person: ").strip().lower().title()

    if company == "" or street == "" or postbox is None or city == "" or holder == "":
        print("Some fields are left empty! Please repeat the entry.")
        time.sleep(2)
        create_account(database)

    # Assign currency to the account.
    exchange = None
    while exchange is None:
        if exchange != "EUR" or exchange != "USD":
            new_account["acc_type"] = exchange = input("Enter the currency of the account (EUR or USD): ").strip().upper()
            break

    input("SAVE? (Press any key) ") 

    # Creating a new account number by checking the previous one
    control_nr = 0
    extract_control = []
    now = datetime.datetime.now()
    format = "%Y-%m"

    for index in database:
        for index_key, index_value in index.items():
            extract_control.append(index_value)
    
    control = extract_control[-3]   
    control_nr = control[-5:] 
    control_nr = int(control_nr)

    """
    Logic of this if statement:
    Comparison of date(year and month) from the last made account in the base with the current date in the system.
    If the slice matches with the previous one we add +1 to the control number (last 5 digits) and typecast it to string.
    If the month(or year) changes, control number resets back to '00001' which is initially a string. 
    """
    if control[3:10] == str(now.strftime(format)):
        print("Control number: ", control_nr)
        control_nr += 1
        new_account["account"] = f"BA-" + str(now.strftime(format)) + "-" + str(f"{control_nr:05d}")
    else:
        control_nr = "00001"
        new_account["account"] = f"BA-" + str(now.strftime(format)) + "-" + control_nr

    # Initial deposit and display of the account number.
    clear()
    print(menu.account_create_balance)
    print("Your account ", new_account["account"], "has been created.\n")
    print("Please enter the deposit amount for your account.\n")

    amount = None
    try:
        new_account["balance"] = amount = int(input("-> "))
    except ValueError or KeyError:
        print("Please enter a numerical amount.")
        return time.sleep(2), amount
    
    new_account["transactions"] = []
    
    database.append(new_account)
    save_database(database, ACCOUNT_PATH)

    # Final information about the created account.
    print(f"Current balance on the account is: ", new_account["balance"], new_account["acc_type"])
    print("To access the account, use the account number and the entered PIN.\n")
    return_to_menu(database)

# Functions to change the account state
def deposit(database):
    clear()
    database = load_database(ACCOUNT_PATH)

    account = input("Please enter the account number: ").strip().upper()
    PIN = int(input("Please enter the PIN: "))
    for index in database:
        if index["PIN"] == PIN and index["account"] == account:
            if index["acc_type"] == "EUR":
                print("Current account balance: ", index["balance"], "€")
                clear()
                print(menu.balance)
                current_time()
                print("Account number", index["account"])
                print("Please enter the amount you want to deposit to the account.")
                print("NOTE! Please use a decimal point, not a comma.")
                try:
                    deposit_amount = int(input("-> "))
                except ValueError:
                    print("Not a numerical entry.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] + deposit_amount
                new_deposit = "+" + str(deposit_amount)
                index["transactions"].append(new_deposit) 
                save_database(database, ACCOUNT_PATH)

            elif index["acc_type"] == "USD":
                print("Current account balance: ", index["balance"], "$")
                clear()
                print(menu.balance)
                current_time()
                print("Account number", index["account"])
                print("Please enter the amount you want to deposit to the account.")
                print("NOTE! Please use a decimal point, not a comma.")
                try:
                    deposit_amount = int(input("-> "))
                except ValueError:
                    print("Not a numerical entry.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] + deposit_amount
                new_deposit = "+" + str(deposit_amount)
                index["transactions"].append(new_deposit) 
                save_database(database, ACCOUNT_PATH)
    else:
        wrong_entry(database)
    print("New account balance is: ", index["balance"])
    return_to_menu(database)

def withdraw(database):
    clear()
    database = load_database(ACCOUNT_PATH)

    account = input("Please enter the account number: ").strip().upper()
    PIN = int(input("Please enter the PIN: ").strip())
    for index in database:
        if index["PIN"] == PIN and index["account"] == account:
            if index["acc_type"] == "EUR":
                print("Current account balance: ", index["balance"], " €")
                clear()
                print(menu.balance)
                current_time()       
                print("Account number", index["account"])
                print("Please enter the amount you want to withdraw from the account.")
                print("NOTE! Please use a decimal point, not a comma.")
                try:
                    withdraw_amount = int(input("-> "))
                except ValueError:
                    print("Not a numerical entry.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] - withdraw_amount
                new_withdraw = "-" + str(withdraw_amount)
                index["transactions"].append(new_withdraw)
                save_database(database, ACCOUNT_PATH) 

            elif index["acc_type"] == "USD":
                print("Current account balance: ", index["balance"], " $")
                clear()
                print(menu.balance)
                current_time()       
                print("Account number", index["account"])
                print("Please enter the amount you want to withdraw.")
                print("NOTE! Please use a decimal point, not a comma.")
                try:
                    withdraw_amount = int(input("-> "))
                except ValueError:
                    print("Not a numerical entry.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] - withdraw_amount
                new_withdraw = "-" + str(withdraw_amount)
                index["transactions"].append(new_withdraw)
                save_database(database, ACCOUNT_PATH) 
    else:
        wrong_entry(database)
    print("New account balance is: ", index["balance"])
    return_to_menu(database)

# Functions for viewing account status
def check_balance(database):
    clear()
    database = load_database(ACCOUNT_PATH)  
    print(menu.balance)
 
    account = input("Please enter the account number: ").strip().upper()
    PIN = int(input("Please enter the PIN: ").strip())    
    clear()            
    print(menu.balance)
    current_time()
    for index in database:
        if index["PIN"] == PIN and index["account"] == account:
            if index["acc_type"] == "EUR":
                print("Current account balance is: ",index["balance"], end="€.")
                break
            elif index["acc_type"] == "USD":
                print("Current account balance is: ",index["balance"], end="$.")
                break
    else:
        wrong_entry(database) 
    return_to_menu(database)

def transactions(database):
    clear()
    database = load_database(ACCOUNT_PATH)

    account = input("Please enter the account number: ").strip().upper()
    PIN = int(input("Please enter the PIN: "))
    clear()
    print(menu.balance)
    current_time()
    for index in database:
        if index["PIN"] == PIN and index["account"] == account:
            if index["acc_type"] == "EUR":
                print(*index["transactions"], sep="€, ", end="€.")
            elif index["acc_type"] == "USD":
                print(*index["transactions"], sep="$, ", end="$.")
            else:
                wrong_entry(database)
    return_to_menu(database)

# Functions to return to the main menu
def return_to_menu(database):
    """
    This function is used to return to the main menu 
    and provide a short message to the user.
    Used in positive outcomes.
    """
    print()
    time.sleep(2)
    input("\nPress any key to return.")
    clear()
    bank.main_menu(database)

def wrong_entry(database):
    """
    This function is used to return to the main menu 
    in case of a negative outcome.
    """
    print("Wrong entry!")
    time.sleep(2)
    clear()
    bank.main_menu(database)  

# Functions for loading and saving data
def save_database(new_account, ACCOUNT_PATH):
    try:
        with open(ACCOUNT_PATH, "w") as file:
            json.dump(new_account, file, indent=4)
    except OSError:
        print("An error occurred. We are very sorry.")

def load_database(ACCOUNT_PATH):
    data = None
    try:
        with open(ACCOUNT_PATH, "r") as file:
            data = json.load(file)
    except OSError:
        print("An error occurred. Sorry.")
    return data
