import time
import GUI as menu
import utils as utils

# Glavni izbornik 
def main_menu(database):
    """
    From here all the major functions are being called up.
    """ 
    print(menu.main_menu)
    choice = input("Vaš izbor: ")
    if choice == "1":
        utils.create_account(database)
    elif choice == "2":  
        utils.balance(database)
    elif choice == "3":
        utils.transactions(database)
    elif choice == "4":  
        utils.deposit(database)       
    elif choice == "5":
        utils.withdraw(database)
    elif choice == "0":
        utils.clear()
        quit(print("Hvala što ste koristili naše usluge. Ugodan dan Vam želimo."))
    else:
        print("Krivi unos. Molimo Vas da unesete jedan od ponuđenih brojeva iz izbornika.")
        time.sleep(2)
        main_menu(database)
    return


# Prizivanje glavnog izbornika u glavnoj funkciji.
def main(database):
    utils.clear()
    main_menu(database)
    return


if __name__ == "__main__":
    database = utils.load_database(utils.ACCOUNT_PATH)
    main(database)

