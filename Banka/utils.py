import json
import datetime
from os import name, system
import GUI as menu
import time
import Banka as bank


ACCOUNT_PATH = "accounts.json"


# Funkcije za bolju preglednost i snalaženje
def clear():
    """   
    This function is called to clear the 
    terminal after every major input event.
    """ 
    if name == 'yes':
        _ = system('cls')
    else:
        _ = system('clear')


def current_time():
    now = datetime.datetime.now()
    format = "%x %X"
    print("Datum i vrijeme: ", now.strftime(format))


# Najkompleksnija funkcija modula - stvaranje novog korisničkog računa.
def create_account(database):
    """
    This function is used to create an user account.
    """
    clear()
    database = load_database(ACCOUNT_PATH)
    print(menu.account_create)
    
    new_account = {}
    company_query = []
    new_account["company"] = company = input("Naziv Tvrtke: ").strip().title() 
    # Checkpoint for company availability 
    for index in database:                
        for user_value in index.items():
            company_query.append(user_value)

    if company in company_query:
        print("Ime tvrtke je zauzeto!")
        time.sleep(2)
        create_account(database)

    # Unos inicijalnih osobnih podataka
    new_account["street"] = street = input("Ulica i broj sjedišta Tvrtke: ").strip().lower().title()
    new_account["PB"] = postbox = int(input("Poštanski broj sjedišta tvrtke: ").strip())
    new_account["HQ"] = city = input("Grad sjedišta Tvrtke: ").strip().lower().title()
    
    try:
       new_account["OIB"] = OIB = int(input("OIB tvrtke: ").strip())
    except ValueError:
        print("Molimo unesite samo brojeve.")
        return time.sleep(2), bank.main_menu(database)

    OIB = str(OIB)
    if len(OIB) != 11:
        print("Molimo unesite pravilan OIB tvrtke, od točno 11 znakova!")
        time.sleep(2)
        create_account(database)
    new_account["account_holder"] = holder = input("Ime i prezime odgovorne osobe: ").strip().lower().title()

    if company == "" or street == "" or postbox == None or city == "" or holder == "":
        print("Neka polja su ostala prazna! Molimo ponovite unos")
        time.sleep(2)
        create_account(database)

    # Dodjela valute računu.
    exchange = None
    while exchange is None:
        if exchange != "EUR" or exchange != "HRK":
            new_account["acc_type"] = exchange = input("Unesite naziv valute računa (EUR ili HRK): ").strip().upper()
            break        
    
    input("SPREMI? (Pritisnite bilo koju tipku) ") 

    # Stvaranje novog broja računa provjerom prethodnog
    control_nr = 0
    extract_control = []
    now = datetime.datetime.now()
    format = "%Y-%m"

    # Hoda kroz bazu i ubacuje vrijednosti u kontrolnu listu. Puno sporije od samog traženja po keyevima 'account' 
    for index in database:
        for index_key, index_value in index.items():
            extract_control.append(index_value)
    
    control = extract_control[-3]   
    control_nr = control[-5:] 
    control_nr = int(control_nr)

    # Logika: uspoređuje datum(godinu i mjesec) iz zadnjeg računa u bazi sa trenutnim datumom iz sistema. 
    # Ako se taj izrezak podudara nadodaje se +1 na kontrolni broj (zadnjih 5 znakova).
    # Ako dođe do promjene mjeseca(ili godine), kontrolni broj se resetira na 00001 koji je u biti string.
    if control[3:10] == str(now.strftime(format)):
        print("Kontrolni broj: ", control_nr)
        control_nr += 1
        new_account["account"] = f"BA-"+ str(now.strftime(format)) + "-" + str(f"{control_nr:05d}")
    else:
        control_nr = "00001"
        new_account["account"] = f"BA-"+ str(now.strftime(format)) +  "-" + control_nr

    #Inicijalni polog i ispis broja računa.
    clear()
    print(menu.account_create_balance)
    print("Vaš račun ", new_account["account"], "je stvoren.\n")
    print("Molimo unesite iznos pologa na Vaš račun\n")

    ovdje = None
    try:
        new_account["balance"] = ovdje = int(input("-> "))
    except ValueError or KeyError:
        print("Molimo Vas, unesite brojčani iznos.")
        return time.sleep(2), ovdje
    
    new_account["transactions"] = []
    
    database.append(new_account)
    save_database(database, ACCOUNT_PATH)

    # Krajnje informacije o stvorenom računu.
    print(f"Trenutno stanje na računu je: ", new_account["balance"], new_account["acc_type"])
    print("Za pristup računu koristite broj računa i uneseni OIB.\n")
    comeback(database)


# Funkcije promjene stanja računa
def deposit(database):
    """
    This functions acts as a deposit function.
    """
    clear()
    database = load_database(ACCOUNT_PATH)

    account = input("Molimo unesite broj računa: ").strip().upper()
    OIB = int(input("Molimo unesite OIB: "))
    for index in database:
        if index["OIB"] == OIB and index["account"] == account:
            if index["acc_type"] == "EUR":
                print("Trenutno stanje računa: ", index["balance"], "€")
                clear()
                print(menu.balance)
                current_time()
                print("Broj računa", index["account"])
                print("Molimo Vas upišite iznos koji želite položiti na račun.")
                print("NAPOMENA! Molimo Vas koristite decimalnu točku, a ne zarez.")
                try:
                    deposit_ammount = int(input("-> "))
                except ValueError:
                    print("Nije brojčani unos.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] + deposit_ammount
                new_deposit = "+" + str(deposit_ammount)
                index["transactions"].append(new_deposit) 
                save_database(database, ACCOUNT_PATH)

            elif index["acc_type"] == "HRK":
                print("Trenutno stanje računa: ", index["balance"], "kn")
                
                clear()
                print(menu.balance)
                current_time()
                print("Broj računa", index["account"])
                print("Molimo Vas upišite iznos koji želite položiti na račun.")
                print("NAPOMENA! Molimo Vas koristite decimalnu točku, a ne zarez.")
                try:
                    deposit_ammount = int(input("-> "))
                except ValueError:
                    print("Nije brojčani unos.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] + deposit_ammount
                new_deposit = "+" + str(deposit_ammount)
                index["transactions"].append(new_deposit) 
                save_database(database, ACCOUNT_PATH)
    else:
        wrong_entry(database)
    print("Novo stanje na računu je: ", index["balance"])
    comeback(database)


def withdraw(database):
    """
    This functions acts as a withdraw function.
    """
    clear()
    database = load_database(ACCOUNT_PATH)
    
    account = input("Molimo unesite broj računa: ").strip().upper()
    OIB = int(input("Molimo unesite OIB: ").strip())
    for index in database:
        if index["OIB"] == OIB and index["account"] == account:
            if index["acc_type"] == "EUR":
                print("Trenutno stanje računa: ", index["balance"], " €")
                clear()
                print(menu.balance)
                current_time()       
                print("Broj računa", index["account"])
                print("Molimo Vas upišite iznos koji želite podignuti s računa.")
                print("NAPOMENA! Molimo Vas koristite decimalnu točku, a ne zarez.")
                try:
                    withdraw_ammount = int(input("-> "))
                except ValueError:
                    print("Nije brojčani unos.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] - withdraw_ammount
                new_withdraw = "-" + str(withdraw_ammount)
                index["transactions"].append(new_withdraw)
                save_database(database, ACCOUNT_PATH) 

            elif index["acc_type"] == "HRK":
                print("Trenutno stanje računa: ", index["balance"], " kn")
                clear()
                print(menu.balance)
                current_time()       
                print("Broj računa", index["account"])
                print("Molimo Vas upišite iznos koji želite podignuti.")
                print("NAPOMENA! Molimo Vas koristite decimalnu točku, a ne zarez.")
                try:
                    withdraw_ammount = int(input("-> "))
                except ValueError:
                    print("Nije brojčani unos.")
                    return time.sleep(2), bank.main_menu(database)
                index["balance"] = index["balance"] - withdraw_ammount
                new_withdraw = "-" + str(withdraw_ammount)
                index["transactions"].append(new_withdraw)
                save_database(database, ACCOUNT_PATH) 

    else:
        wrong_entry(database)
    print("Novo stanje na računu je: ", index["balance"])
    comeback(database)

# Funkcije pregleda stanja računa
def balance(database):
    """
    This function is used to see the current balance on the account.
    """
    clear()
    database = load_database(ACCOUNT_PATH)  
    print(menu.balance)
 
    account = input("Molimo unesite broj računa: ").strip().upper()
    OIB = int(input("Molimo unesite OIB: ").strip())    
    clear()            
    print(menu.balance)
    current_time()
    for index in database:
        if index["OIB"] == OIB and index["account"] == account:
            if index["acc_type"] == "EUR":
                print("Trenutno stanje na računu je: ",index["balance"], end="€.")
                break
            elif index["acc_type"] == "HRK":
                print("Trenutno stanje na računu je: ",index["balance"], end="kn.")
                break
    else:
        wrong_entry(database) 
    comeback(database)


def transactions(database):
    """
    This function is used to see the transaction history of the account.
    """
    clear()
    database = load_database(ACCOUNT_PATH)

    account = input("Molimo unesite broj računa: ").strip().upper()
    OIB = int(input("Molimo unesite OIB: "))
    clear()
    print(menu.balance)
    current_time()
    for index in database:
        if index["OIB"] == OIB and index["account"] == account:
            if index["acc_type"] == "EUR":
                print(*index["transactions"], sep="€, ", end="€.")
            elif index["acc_type"] == "HRK":
                print(*index["transactions"], sep="kn, ", end="kn.")
            else:
                wrong_entry(database)
    comeback(database)

# Funkcije povratka na glavni izbornik
def comeback(database):
    """
    This function is used to return to main menu 
    and provide a short message to the user.
    Used in positive outcomes.
    """
    print()
    time.sleep(2)
    input("\nPritisnite bilo koju tipku za povratak.")
    clear()
    bank.main_menu(database)


def wrong_entry(database):
    """
    This function is used to return to 
    main menu in case of a negative outcome
    """
    print("Krivi unos!")
    time.sleep(2)
    clear()
    bank.main_menu(database)  


# Funkcije za učitavanje i spremanje podataka 
def save_database(new_account, ACCOUNT_PATH):
    try:
        with open(ACCOUNT_PATH, "w") as file:
            json.dump(new_account, file, indent=4)
    except OSError:
        print("Desila se pogreška pri spremanju datoteke.")


def load_database(ACCOUNT_PATH):
    data = None
    try:
        with open(ACCOUNT_PATH, "r") as file:
            data = json.load(file)
    except OSError:
        print("Desila se pogreška pri učitavanju datoteke.")
    return data
