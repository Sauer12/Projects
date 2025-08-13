class InsuredPerson():
    def __init__(self, name, surname, age, phone_number):
        self.name = name
        self.surname = surname
        self.age = age
        self.phone_number = phone_number

    def __str__(self):
        return f"{self.name}   {self.surname}   {self.age}   {self.phone_number}"