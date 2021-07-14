import time
from random import randint
from syndicate import Syndicate

class Company:
    employees = {}

    def genId():
        id = 0
        while id in Company.employees:
            id = randint(0, 99)
        return id

    def addEmployee(new):
        Company.employees[new.id] = new
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        for employee in Company.employees.values():
            print(employee)
        print("\n")

    def removeEmployee(id):
        del Company.employees[id]

