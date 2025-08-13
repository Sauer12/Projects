import re

from database_of_insured_persons import DatabaseOfInsuredPersons
from insured_person import InsuredPerson



database_of_insured_persons = DatabaseOfInsuredPersons()

# Pridanie nového poistenca do kolekcie v triede DatabaseOfInsuredPersons a validácia prázdneho vstupu
def add_insured_person(db):
    name = input("Zadajte meno poistenca: ").strip()
    if not name:
        print("Meno nemôže byť prázdne.")
        return

    surname = input("Zadajte priezvisko poistenca: ").strip()
    if not surname:
        print("Priezvisko nemôže byť prázdne.")
        return

    age = input("Zadajte vek poistenca: ").strip()
    if not age.isdigit() or int(age) <= 0:
        print("Vek musí byť kladné celé číslo.")
        return

    phone_number = input("Zadajte telefónne číslo poistenca: ").strip()
    normalized_phone_number = phone_number.replace(" ", "")
    if not normalized_phone_number.isdigit() or (len(normalized_phone_number) < 10 or len(normalized_phone_number) > 10):
        print("Telefónne číslo musí obsahovať aspoň 10 číslic.")
        return

    insured_person = InsuredPerson(name, surname, age, normalized_phone_number)
    db.add_insured_person(insured_person)

# Vypíše všetkých poistencov v kolekcii v triede DatabaseOfInsuredPersons
def list_insured_persons(db):
    if not db.insured_persons:
        print("Zoznam poistencov je prázdny.")
    else:
        db.show_insured_persons()

# Vyhľadá poistenca podľa mena a priezviska v kolekcii v triede DatabaseOfInsuredPersons
def show_insured_persons(db):
    name = input("Zadajte meno poistenca: ")
    surname = input("Zadajte meno poistenca: ")
    insured_person = db.search_insured_person(name, surname)
    if insured_person:
        print(f"\nNájdený poistenec: {insured_person}")
    else:
        print("Poistenec nebol nájdený v databáze.")

# Hlavný program, ktorý umožňuje používateľovi vybrať si možnosť z menu
choice = ""
while choice != "4":
    print()
    print("_" * 30)
    print("Evidencia pojistených osôb")
    print("_" * 30)
    print("Vyberte si možnosť:")
    print("1. Pridať nového poistenca")
    print("2. Vypísať všetkých poistencov")
    print("3. Vyhľadať poistenca")
    print("4. Ukončiť program\n")
    choice = input("Zadajte možnosť: ")

    match choice:
        case "1":
            add_insured_person(database_of_insured_persons)
        case "2":
            list_insured_persons(database_of_insured_persons)
        case "3":
            show_insured_persons(database_of_insured_persons)
        case "4":
            print("Ukončujem program.")
            choice = "4"
        case _:
            print("Neplatná možnosť, skúste znova.")
