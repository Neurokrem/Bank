import time
import GUI as menu
import utils as utils

# Main menu
def main_menu(database):
    """
    From here all the major functions are being called up.
    """ 
    print(menu.main_menu)
    choice = input("Your choice: ")
    if choice == "1":
        utils.create_account(database)
    elif choice == "2":  
        utils.check_balance(database)
    elif choice == "3":
        utils.view_transactions(database)
    elif choice == "4":  
        utils.deposit(database)       
    elif choice == "5":
        utils.withdraw(database)
    elif choice == "0":
        utils.clear()
        quit(print("Thank You for using our services. Have a great day!"))
    else:
        print("Wrong input. Please enter one of the provided numbers from the menu.")
        time.sleep(2)
        main_menu(database)
    return

# Calling the main menu in the main function.
def main(database):
    utils.clear()
    main_menu(database)
    return

if __name__ == "__main__":
    database = utils.load_database(utils.ACCOUNT_PATH)
    main(database)
