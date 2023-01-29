import openpyxl
from datetime import datetime, timedelta

import pandas as pd

# MODE SWITCH / MAIN
def switch_mode():
    print('''
Andrija, sta ti se sad radi?
1 - unesi korisnika
2 - ko ti duguje
3 - koliko si zaradio
4 - neko ti je platio, a?
5 - pretrazi po nazivu rada
6 - gotovo :-(
    ''')
    
    while True:
        try:
            mode = int(input("Biraj: "))
            break
        except ValueError:
            print("Samo brojevi jebes ga...")
        
    if mode == 1:
        insert_data()

    elif mode == 2:
        read_unpaid()

    elif mode == 3:
        read_profit()

    elif mode == 4:
        update_paid()

    elif mode == 5:
        search()

    elif mode == 6:
        end()

    else:
        print("Daj ne zajebavaj, dao sam ti opcije, unesi ljudski...")
        switch_mode()


# MODE DEFINITON

#INSERTION
def insert_data(next_param = "DA"):
    next = next_param

    if next == "DA":
        workbook = openpyxl.open("data.xlsx")
        sheet = workbook.active

        ime = input("Andrija, unesi ime i prezime svog klijenta: ")
        mejl = input("Andrija, unesi mejl svog klijenta: ")
        rad = input("Andrija, unesi ime rada svog kliejnta: ")

        while True:
            try:
                cena = int(input("Andrija, unesi cenu rada koji radis: "))
                break
            except ValueError:
                print("Je l ti to lici na cenu decu ti rasadnicku? Brojevi, Andrija, BROJEVI... ")
        datum_uneto = datetime.today().strftime("%d-%m-%Y")
        datum_placeno = None

        print("Andrija, proveri podatke koje si uneo za svaki slucaj...")

        sure = input('''
Ako si siguran moze samo Enter, a ako nisi, 
lupi glavom u tastaturu pa onda Enter da probas opet. \n''')

        if sure == "":
            sheet.append((ime, mejl, rad, cena, datum_uneto, datum_placeno, False))
            workbook.save(filename="data.xlsx")

            next = input("Ima li jos ljudi, vojnice? (da/ne): ").upper()
            insert_data(next)
        
        else:
            insert_data()


    elif next == "NE":
        next_check()

    else:
        print("Daj ne zajebavaj, dao sam ti opcije, unesi ljudski...")
        next = input("Ima li jos ljudi, vojnice? (da/ne): ").upper()
        insert_data(next)


#CONTINUE OR NO
def next_check():
    next = input("\n\nCes jos nesto? (da/ne): ").upper()

    while next not in ("DA", "NE"):
        print("Daj ne zajebavaj, dao sam ti opcije, unesi ljudski...")
        next = input("\n\nCes jos nesto? (da/ne): ").upper()

    if next == "DA":
        switch_mode()
    elif next == "NE":
        end()


#DEBT EXPLORATION
def read_unpaid():
    print("Sad cemo videti ko su ti shabani...")

    df = pd.read_excel("data.xlsx")
    unpaid_df = df[df["PLACENO"] == False]

    print(unpaid_df[["IME I PREZIME", "E-MAIL", "RAD", "CENA", "DATUM UNOSA"]])

    next_check()


#PROFIT EXPLORATION
def read_profit():
    print("Broje se parice... skupo, skupo...")
    print('''
Koji vremenski period ti je u interesu?
1 - protekla nedelja
2 - protekli mesec
3 - proteklih nekoliko dana
4 - odredjeni mesec
''')
    wanted_period = 5
    while True:
        try:
            while wanted_period > 4 or wanted_period <= 0:
                wanted_period = int(input("Kazi bratu broj od 1 do 4...: "))
            break
        
        except ValueError:
            print("Daj ne zajebavaj, dao sam ti opcije, unesi ljudski...")

    if wanted_period == 1:
        period = 7

    elif wanted_period == 2:
        period = 31

    elif wanted_period == 3:
        while True:
            try:
                period = int(input("Mnogo ga komplikujes. Koliko dana?: "))
                break
        
            except ValueError:
                print("Aj bar unesi BROJ dana...")

    elif wanted_period == 4:
        month_num = 13
        while True:
            try:
                while month_num > 12 or month_num <= 0:
                    month_num = int(input("Koji mesec? Numericki, molim te (1-12): "))
                break
        
            except ValueError:
                print("Rekoh numericki...")

    df = pd.read_excel("data.xlsx")
    df["DATUM UNOSA"] = pd.to_datetime(df["DATUM UNOSA"], infer_datetime_format=True)

    if wanted_period < 4:
        today = datetime.today()
        before = datetime.today() - timedelta(days=period)

        df = df[(df['DATUM UNOSA'] > before) & (df['DATUM UNOSA'] <= today)]

        paid_df = df[df["PLACENO"] == True]
    
        paid_profit = paid_df["CENA"].sum()
        full_profit = df["CENA"].sum()
    
    else:
        if month_num < 10:
            month = f"0{month_num}"

        else:
            month = f"{month_num}"

        df = df[df['DATUM UNOSA'].dt.strftime('%m') == '01']

        paid_df = df[df["PLACENO"] == True]
    
        paid_profit = paid_df["CENA"].sum()
        full_profit = df["CENA"].sum()


    if paid_profit != full_profit:
        print(f"Zaradio si {paid_profit} dinara, ali da su ti svi platili, bilo bi to {full_profit}...")
    
    else:
        print(f"Sve se vratilo, sve se platilo... Tvoja zarada je {paid_profit} dinara. ")

    next_check()


#UPDATE PAID
def update_paid():
    print("Ko je od ovih krembila ispostovao brata? ")

    df = pd.read_excel("data.xlsx")
    df["DATUM UNOSA"] = pd.to_datetime(df["DATUM UNOSA"], infer_datetime_format=True)

    unpaid_df = df[df["PLACENO"] == False]

    print(unpaid_df[["IME I PREZIME", "E-MAIL", "RAD"]])

    ids = input("Unesi ID (mozes i vise ID-eva odvojenih jednim spejsom): ")
    ids = ids.split(' ')
    
    workbook = openpyxl.open("data.xlsx")
    sheet = workbook.active

    for id in ids:
        sheet_row = int(id) + 2
        sheet[f"F{sheet_row}"] = datetime.today().strftime("%d-%m-%Y")
        sheet[f"G{sheet_row}"] = True
        
    workbook.save(filename="data.xlsx")

    next_check()

def search():
    print("Verovatno ti niko nije trazio da pises seminarski o golom Nik Kejdzu...")
    pattern = input("Ajde kazi da vidimo o cemu je moguce da neko jeste to uradio: ")

    df = pd.read_excel("data.xlsx")
    df = df[df["RAD"].str.contains(pattern)]
    
    if len(df) != 0:
        print(df[["IME I PREZIME", "RAD"]])

    else:
        print(f"Nema radova koji sadrze '{pattern}'.")

    next_check()


#CLOSE
def end():
    print("Do sledeceg vidjenja...")


switch_mode()
