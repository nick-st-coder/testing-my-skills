#d age = input("Enter your age here: ")

# txt = f"Hello, you're {age} years old"
# print (txt)

# class Myclass:
#     def __init__(self, mark, color, year):
#         self.mark = mark
#         self.color = color
#         self.year = year
#     def execute(self):
#         print (f"This car is {self.mark}, it's {self.color} color and {self.year} year")  

# car1 = Myclass("BMW", "red", 2020)
# car2 = Myclass("Skoda", "green", 2018)
# car3 = Myclass("Lada", "blue", 1990)

# car1.execute()
# car2.execute()
# car3.execute()

class Person:
    def __init__(self, firstname, lastname):
        
        self.fname = firstname
        self.lname = lastname
    def printname (self):
        print(f"Twoje imie: {self.fname} oraz twoje nazwisko: {self.lname}") 

firstper = Person("Anna", "Naziwsko")
firstper.printname()

class Student(Person):
    def __init__(self, firstname, lastname, year):
        super().__init__(firstname, lastname)
        self.gradyear = year 
    def welcome (self):
        print(f"Twoje imie: {self.fname} oraz twoje nazwisko: {self.lname} oraz {self.gradyear}")  

obj = Student("Hello", "Hi", 2012)
obj.welcome(Person)
