class DatabaseOfInsuredPersons():
    def __init__(self):
        self.insured_persons = []

    # Pridanie poistenca do databázy
    def add_insured_person(self, insured_person):
        if insured_person not in self.insured_persons:
            self.insured_persons.append(insured_person)
        else:
            print("Insured person already exists in the database.")

    # Vypíše všetkých poistencov v databáze
    def show_insured_persons(self):
        for insured_person in self.insured_persons:
            print(insured_person)

    # Vyhľadá poistenca podľa mena a priezviska v databáze
    def search_insured_person(self, name, surname):
        for insured_person in self.insured_persons:
            if insured_person.name == name and insured_person.surname == surname:
                return insured_person
        return None

